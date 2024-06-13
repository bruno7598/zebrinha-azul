import os
import json
import yaml
from easydict import EasyDict as edict
from v1.modules.singleton import Singleton

class Settings(metaclass=Singleton):
    def __init__(self):
        self.MODE_DEPLOY = "development"
        self.API_KEY_TEMP = ""
        self.API_KEY_TRAFFIC = ""
        self.capitals = {}

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def load(self, env, api_key_temp, api_key_traffic):
        self.MODE_DEPLOY = env
        self.API_KEY_TEMP = api_key_temp
        self.API_KEY_TRAFFIC = api_key_traffic

        config_path = os.path.join(os.path.dirname(__file__), "config", "environment.yaml")
        with open(config_path, 'r') as sc:
            config = yaml.safe_load(sc)
            self.__dict__.update(edict(config[env]))

        capitals_path = os.path.join(os.path.dirname(__file__), "v1", "resource", "schema_capitals.json")
        with open(capitals_path, 'r') as f:
            self.capitals = json.load(f).get("capitals")