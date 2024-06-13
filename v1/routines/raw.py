import asyncio
import aiohttp

from datetime import datetime, timedelta
from settings import Settings

from v1.modules.utils import translate_directions_data

class Raw:

    def __init__(self):
        self.cfg = Settings()

    async def fetch(self, session, url, params):
        async with session.get(url, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return {"status_code": response.status, "error_message": await response.text()}

    async def get_weather(self, session, coords, timestamp):
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            'lat': coords['lat'],
            'lon': coords['lon'],
            'appid': self.cfg.API_KEY_TEMP,
            'units': 'metric',
            'lang': 'pt',
            'dt': timestamp
        }
        return await self.fetch(session, url, params)

    async def get_traffic(self, session, origin_coords, destination_coords, timestamp):
        url = "https://maps.googleapis.com/maps/api/directions/json"
        params = {
            "origin": f"{origin_coords['lat']},{origin_coords['lon']}",
            "destination": f"{destination_coords['lat']},{destination_coords['lon']}",
            "departure_time": timestamp,
            "key": self.cfg.API_KEY_TRAFFIC
        }
        return await self.fetch(session, url, params)

    async def routines_temp(self, execution_date):
        date_hours = datetime.strptime(execution_date, '%Y-%m-%d %H:%M')
        timestamp = int(date_hours.timestamp())

        weather_data_all = {}
        async with aiohttp.ClientSession() as session:
            tasks = []
            for cidade, coords in self.cfg.capitals.items():
                tasks.append(self.get_weather(session, coords, timestamp))
            
            responses = await asyncio.gather(*tasks)

            for i, (cidade, coords) in enumerate(self.cfg.capitals.items()):
                climas = responses[i]
                if 'status_code' in climas:
                    weather_data_all[cidade] = {"Erro": climas['error_message']}
                else:
                    info_climatica = {
                        "Coordenadas Geográficas": {
                            "Latitude": coords['lat'],
                            "Longitude": coords['lon']
                        },
                        "Condições Climáticas Atuais": {
                            "Descrição": climas['weather'][0]['description'],
                            "Temperatura": climas['main']['temp'],
                            "Sensação Térmica": climas['main']['feels_like'],
                            "Pressão Atmosférica": climas['main']['pressure'],
                            "Umidade": climas['main']['humidity'],
                            "Velocidade do Vento": climas['wind']['speed'],
                            "Direção do Vento": climas['wind']['deg']
                        }
                    }
                    weather_data_all[cidade] = info_climatica

        return weather_data_all

    async def routines_traffic(self, execution_date):
        date_hours = datetime.strptime(execution_date, '%Y-%m-%d %H:%M')
        if date_hours <= datetime.now():
            date_hours = datetime.now() + timedelta(days=1)
        timestamp = int(date_hours.timestamp())

        traffic_data_all = {}
        async with aiohttp.ClientSession() as session:
            tasks = []
            capitals = list(self.cfg.capitals.items())
            for i in range(len(capitals)):
                for j in range(i + 1, len(capitals)):
                    origin_name, origin_coords = capitals[i]
                    destination_name, destination_coords = capitals[j]
                    tasks.append(
                        self.get_traffic(session, origin_coords, destination_coords, timestamp)
                    )
            
            responses = await asyncio.gather(*tasks)

            for i, (origin_name, origin_coords) in enumerate(capitals):
                for j, (destination_name, destination_coords) in enumerate(capitals[i + 1:]):
                    route_data = responses.pop(0)
                    if 'status_code' in route_data:
                        traffic_data_all[f"{origin_name} -> {destination_name}"] = {
                            "message": "Falha ao obter a rota",
                            "status_code": route_data['status_code'],
                            "error_message": route_data['error_message']
                        }
                    else:
                        traffic_data_all[f"{origin_name} -> {destination_name}"] = route_data

        return traffic_data_all

    def run_routines(self, execution_date):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        weather_data = new_loop.run_until_complete(self.routines_temp(execution_date))
        traffic_data = new_loop.run_until_complete(self.routines_traffic(execution_date))
        traffic_data = translate_directions_data(traffic_data)
        new_loop.close()
        return weather_data, traffic_data