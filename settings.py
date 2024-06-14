import os
import json
import yaml
from easydict import EasyDict as edict
from v1.modules.singleton import Singleton

class Settings(metaclass=Singleton):
    def __init__(self):
        self.MODE_DEPLOY = "dev"
        self.API_KEY_TEMP = ""
        self.API_KEY_TRAFFIC = ""
        self.capitals = {}
        self.DB_HOST = ""
        self.DB_NAME = ""
        self.DB_USER = ""
        self.DB_PASSWORD = ""
        self.DB_TABLE = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def load(self, env, api_key_temp, api_key_traffic, db_host, db_name, db_user, db_password):
        self.MODE_DEPLOY = env
        self.API_KEY_TEMP = api_key_temp
        self.API_KEY_TRAFFIC = api_key_traffic
        self.DB_HOST = db_host
        self.DB_NAME = db_name
        self.DB_USER = db_user
        self.DB_PASSWORD = db_password

        config_path = os.path.join(os.path.dirname(__file__), "config", "environment.yaml")
        with open(config_path, 'r') as sc:
            config = yaml.safe_load(sc)
            self.__dict__.update(edict(config[env]))

        capitals_path = os.path.join(os.path.dirname(__file__), "v1", "resource", "schema_capitals.json")
        with open(capitals_path, 'r') as f:
            self.capitals = json.load(f).get("capitals")