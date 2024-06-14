import json
from flask import request
from flask_restful import Resource

from v1.model.execution_date import ExecutionDate
from v1.routines.raw import Raw

class GetRaw(Resource):
    def __init__(self) -> None:
        self.raw = Raw()

    def post(self):
        payload = request.json
        execution_date = payload.get('execution_date')

        try:
            ExecutionDate(execution_date=execution_date)
        except ValueError as e:
            return {"message": str(e)}, 400

        temp_data, traffic_data = self.raw.run_routines(execution_date)

        if "Erro" not in temp_data.values() and "message" not in traffic_data.values():
            return {"message": "JSONs salvos com sucesso"}, 200
        else:
            return {
                "message": "Falha ao obter os dados do tempo ou de tráfego",
                "temp_data": temp_data,
                "traffic_data": traffic_data,
                "status_code": 500
            }, 500