import json
from flask import request
from flask_restful import Resource

from v1.model.execution_date import ExecutionDate
from v1.routines.application import Application

class GetRaw(Resource):
    def __init__(self) -> None:
        self.application = Application()

    def post(self):
        payload = request.json
        execution_date = payload.get('execution_date')

        try:
            ExecutionDate(execution_date=execution_date)
        except ValueError as e:
            return {"message": str(e)}, 400

        execution_date_clean = execution_date.replace('-', '').replace(':', '').replace(' ', '')

        result = self.application(execution_date_clean)

        if "Erro" not in result and "message" not in result:

            return {"message": "JSONs salvos com sucesso"}, 200
        else:
            return {
                "message": "Falha ao obter os dados do tempo ou de tráfego",
                "status_code": 500
            }, 500