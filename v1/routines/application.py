import os
import psycopg2

class Application:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="your_host",
            database="your_database",
            user="your_user",
            password="your_password"
        )
        self.cursor = self.conn.cursor()

    def routines(self, execution_date):
        breakpoint()
        for filename in os.listdir("/home/bruno7598/project/zebrinha-azul/v1/resource/json_raw"):
            if filename.startswith(str(execution_date)):
                full_path = os.path.join("/home/bruno7598/project/zebrinha-azul/v1/resource/json_raw", filename)
                self.insert_into_postgresql(full_path)

    def insert_into_postgresql(self, file_path):
        with open(file_path, 'r') as file:
            data = file.read()
            sql_command = "INSERT INTO your_table (date, content) VALUES (%s, %s)"
            self.cursor.execute(sql_command, (self.execution_date, data))
            self.conn.commit()

    def close_connection(self):
        self.cursor.close()
        self.conn.close()