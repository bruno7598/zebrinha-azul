from flask import Blueprint
from flask_restful import Api

# from v1.services.get_application import GetApplication
# from v1.services.get_conform import GetConform
from v1.services.get_raw import GetRaw
# from v1.services.get_standardized import GetStandardized

api_bp = Blueprint("api", __name__)
api = Api(api_bp)

api.add_resource(GetRaw, "/raw")
# api.add_resource(GetStandardized, "/standardized")
# api.add_resource(GetConform, "/conform")
# api.add_resource(GetApplication, "/application")