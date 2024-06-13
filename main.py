import os
from flask import Flask
from settings import Settings
from v1.app import api_bp

env = os.getenv("MODE_DEPLOY", "dev")
api_key_temp = os.getenv("API_KEY_TEMP", "")
api_key_traffic = os.getenv("API_KEY_TRAFFIC", "")

settings = Settings()

settings.load(env, api_key_temp, api_key_traffic)

def create_app():
    app = Flask(__name__)

    app.register_blueprint(api_bp, url_prefix='/v1')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8000)