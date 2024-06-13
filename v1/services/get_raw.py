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

        execution_date_clean = execution_date.replace('-', '').replace(':', '').replace(' ', '')

        temp_data, traffic_data = self.raw.run_routines(execution_date)

        if "Erro" not in temp_data.values() and "message" not in traffic_data.values():
            temp_filename = f'/home/bruno7598/project/zebrinha-azul/v1/resource/json_raw/temp_data_{execution_date_clean}.json'
            traffic_filename = f'/home/bruno7598/project/zebrinha-azul/v1/resource/json_raw/traffic_data_{execution_date_clean}.json'

            with open(temp_filename, 'w') as f:
                json.dump(temp_data, f)

            with open(traffic_filename, 'w') as f:
                json.dump(traffic_data, f)

            return {"message": "JSONs salvos com sucesso"}, 200
        else:
            return {
                "message": "Falha ao obter os dados do tempo ou de tráfego",
                "temp_data": temp_data,
                "traffic_data": traffic_data,
                "status_code": 500
            }, 500