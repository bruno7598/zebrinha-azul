from flask import request
from flask_restful import Resource

from v1.model.execution_date import ExecutionDate
from v1.routines.application import Application

class GetApplication(Resource):
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

        try:
            self.application.routines(execution_date_clean)
            print("Dados inseridos/atualizados com sucesso no PostgreSQL!")
        except Exception as e:
            print(f"Erro ao inserir/atualizar dados no PostgreSQL: {str(e)}")
        finally:
            self.application.close_connection()