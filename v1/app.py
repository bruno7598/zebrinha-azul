from flask import Blueprint
from flask_restful import Api

from v1.services.get_raw import GetRaw
from v1.services.get_application import GetApplication


api_bp = Blueprint("api", __name__)
api = Api(api_bp)

api.add_resource(GetRaw, "/raw")
api.add_resource(GetApplication, "/application")
