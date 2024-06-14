import os
import json
import psycopg2
from settings import Settings

class Application:
    def __init__(self):
        """
        Initialize the Application with PostgreSQL connection settings.
        """
        self.cfg = Settings()
        self.conn = psycopg2.connect(
            host=self.cfg.DB_HOST,
            database=self.cfg.DB_NAME,
            user=self.cfg.DB_USER,
            password=self.cfg.DB_PASSWORD
        )
        self.cursor = self.conn.cursor()

    def routines(self, execution_date):
        """
        Process JSON files and insert weather or routes data into PostgreSQL based on filename.
        
        Args:
            execution_date (str): The execution date used to filter files.
        """
        directory = "./json_raw"
        for filename in os.listdir(directory):
            full_path = os.path.join(directory, filename)
            if "weather" in filename:
                self.insert_weather_into_postgresql(full_path, execution_date)
            elif "routes" in filename:
                self.insert_routes_into_postgresql(full_path)

    def insert_weather_into_postgresql(self, file_path, execution_date):
        """
        Insert weather data from a JSON file into the PostgreSQL database.
        
        Args:
            file_path (str): The path to the JSON file containing weather data.
            execution_date (str): The execution date to be associated with the data.
        """
        with open(file_path, 'r') as file:
            weather_data = json.load(file)

        for city, city_data in weather_data.items():
            coordinates = city_data['Coordenadas Geográficas']
            conditions = city_data['Condições Climáticas Atuais']

            sql_command = f"""
            INSERT INTO {self.cfg.tables_weather} (city, latitude, longitude, description, temperature, feels_like, pressure, humidity, wind_speed, wind_direction)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            try:
                self.cursor.execute(sql_command, (city, coordinates['Latitude'], coordinates['Longitude'],
                                                  conditions['Descrição'], conditions['Temperatura'], conditions['Sensação Térmica'],
                                                  conditions['Pressão Atmosférica'], conditions['Umidade'],
                                                  conditions['Velocidade do Vento'], conditions['Direção do Vento']))
                self.conn.commit()
                print(f"Weather data for {city} inserted successfully!")
            except psycopg2.Error as e:
                self.conn.rollback()
                print(f"Error inserting weather data for {city}: {e}")

    def insert_routes_into_postgresql(self, file_path):
        """
        Insert routes data from a JSON file into the PostgreSQL database.
        
        Args:
            file_path (str): The path to the JSON file containing routes data.
        """
        with open(file_path, 'r') as file:
            routes_data = json.load(file)

        for route, route_data in routes_data.items():
            origin_city, destination_city = route.split(" -> ")

            for waypoint in route_data['Geocoded Waypoints']:
                geocoder_status = waypoint['geocoder_status']
                place_id = waypoint['place_id']
                types = waypoint['types']

                bounds_northeast_lat = route_data['Routes'][0]['Bounds']['northeast']['lat']
                bounds_northeast_lng = route_data['Routes'][0]['Bounds']['northeast']['lng']
                bounds_southwest_lat = route_data['Routes'][0]['Bounds']['southwest']['lat']
                bounds_southwest_lng = route_data['Routes'][0]['Bounds']['southwest']['lng']

                copyrights = route_data['Routes'][0]['Copyrights']

                for leg in route_data['Routes'][0]['Legs']:
                    leg_distance = leg['Distance']
                    leg_duration = leg['Duration']
                    leg_end_address = leg['End Address']
                    leg_end_location_lat = leg['End Location']['lat']
                    leg_end_location_lng = leg['End Location']['lng']
                    leg_start_address = leg['Start Address']
                    leg_start_location_lat = leg['Start Location']['lat']
                    leg_start_location_lng = leg['Start Location']['lng']

                    for step in leg['Steps']:
                        step_instructions = step['Instructions']
                        step_distance = step['Distance']
                        step_duration = step['Duration']
                        step_end_location_lat = step['End Location']['lat']
                        step_end_location_lng = step['End Location']['lng']
                        step_start_location_lat = step['Start Location']['lat']
                        step_start_location_lng = step['Start Location']['lng']
                        step_travel_mode = step['Travel Mode']

                        sql_command = f"""
                        INSERT INTO {self.cfg.tables_route} (origin_city, destination_city, geocoder_status, place_id, types,
                                                bounds_northeast_lat, bounds_northeast_lng, bounds_southwest_lat, bounds_southwest_lng,
                                                copyrights, leg_distance, leg_duration, leg_end_address, leg_end_location_lat,
                                                leg_end_location_lng, leg_start_address, leg_start_location_lat, leg_start_location_lng,
                                                step_instructions, step_distance, step_duration, step_end_location_lat,
                                                step_end_location_lng, step_start_location_lat, step_start_location_lng, step_travel_mode)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
                        try:
                            self.cursor.execute(sql_command, (origin_city, destination_city, geocoder_status, place_id, types,
                                                             bounds_northeast_lat, bounds_northeast_lng, bounds_southwest_lat, bounds_southwest_lng,
                                                             copyrights, leg_distance, leg_duration, leg_end_address, leg_end_location_lat,
                                                             leg_end_location_lng, leg_start_address, leg_start_location_lat, leg_start_location_lng,
                                                             step_instructions, step_distance, step_duration, step_end_location_lat,
                                                             step_end_location_lng, step_start_location_lat, step_start_location_lng, step_travel_mode))
                            self.conn.commit()
                            print(f"Route data {origin_city} -> {destination_city} inserted successfully!")
                        except psycopg2.Error as e:
                            self.conn.rollback()
                            print(f"Error inserting route data {origin_city} -> {destination_city}: {e}")

    def close_connection(self):
        """
        Close the cursor and PostgreSQL database connection.
        """
        self.cursor.close()
        self.conn.close()