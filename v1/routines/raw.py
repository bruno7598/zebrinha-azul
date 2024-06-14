import json
import asyncio
import aiohttp
from datetime import datetime, timedelta
from settings import Settings
from v1.modules.utils import translate_directions_data

class Raw:
    def __init__(self):
        """Initialize with configuration settings."""
        self.cfg = Settings()

    async def fetch(self, session, url, params):
        """
        Fetch data from a given URL with parameters using an aiohttp session.
        
        Args:
            session (aiohttp.ClientSession): The aiohttp session to use.
            url (str): The URL to fetch data from.
            params (dict): The parameters to include in the request.
        
        Returns:
            dict: The JSON response data or error information.
        """
        async with session.get(url, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return {"status_code": response.status, "error_message": await response.text()}

    async def get_weather(self, session, coords, timestamp):
        """
        Get weather data for a specific location and time.
        
        Args:
            session (aiohttp.ClientSession): The aiohttp session to use.
            coords (dict): The coordinates with 'lat' and 'lon'.
            timestamp (int): The timestamp for the weather data.
        
        Returns:
            dict: The weather data response.
        """
        url = self.cfg.api_weather
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
        """
        Get traffic data between two locations for a specific time.
        
        Args:
            session (aiohttp.ClientSession): The aiohttp session to use.
            origin_coords (dict): The origin coordinates with 'lat' and 'lon'.
            destination_coords (dict): The destination coordinates with 'lat' and 'lon'.
            timestamp (int): The timestamp for the traffic data.
        
        Returns:
            dict: The traffic data response.
        """
        url = self.cfg.api_route
        params = {
            "origin": f"{origin_coords['lat']},{origin_coords['lon']}",
            "destination": f"{destination_coords['lat']},{destination_coords['lon']}",
            "departure_time": timestamp,
            "key": self.cfg.API_KEY_TRAFFIC
        }
        return await self.fetch(session, url, params)

    async def routines_temp(self, execution_date):
        """
        Fetch weather data for all configured capital cities at a specific date and time.
        
        Args:
            execution_date (str): The date and time in the format '%Y-%m-%d %H:%M'.
        
        Returns:
            dict: The weather data for all capitals.
        """
        date_hours = datetime.strptime(execution_date, '%Y-%m-%d %H:%M')
        timestamp = int(date_hours.timestamp())

        weather_data_all = {}
        async with aiohttp.ClientSession() as session:
            tasks = [self.get_weather(session, coords, timestamp) for cidade, coords in self.cfg.capitals.items()]
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
        """
        Fetch traffic data between all pairs of configured capital cities for a specific date and time.
        
        Args:
            execution_date (str): The date and time in the format '%Y-%m-%d %H:%M'.
        
        Returns:
            dict: The traffic data for all routes between capitals.
        """
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
                    tasks.append(self.get_traffic(session, origin_coords, destination_coords, timestamp))
            
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
        """
        Run both weather and traffic data routines, save results to files, and return success status.
        
        Args:
            execution_date (str): The date and time in the format '%Y-%m-%d %H:%M'.
        
        Returns:
            str: "success"
        """
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        weather_data = new_loop.run_until_complete(self.routines_temp(execution_date))
        traffic_data = new_loop.run_until_complete(self.routines_traffic(execution_date))
        traffic_data = translate_directions_data(traffic_data)
        self.insertion_data(execution_date, weather_data, traffic_data)
        new_loop.close()
        
        return "success"
    
    def insertion_data(self, execution_date, temp_data, traffic_data):
        """
        Save weather and traffic data to JSON files.
        
        Args:
            execution_date (str): The date and time in the format '%Y-%m-%d %H:%M'.
            temp_data (dict): The weather data to save.
            traffic_data (dict): The traffic data to save.
        
        Returns:
            str: "success"
        """
        execution_date_clean = execution_date.replace('-', '').replace(':', '').replace(' ', '')
        temp_filename = f'./json_raw/temp_data_{execution_date_clean}.json'
        traffic_filename = f'./json_raw/traffic_data_{execution_date_clean}.json'

        with open(temp_filename, 'w') as f:
            json.dump(temp_data, f)

        with open(traffic_filename, 'w') as f:
            json.dump(traffic_data, f)

        return "success"
