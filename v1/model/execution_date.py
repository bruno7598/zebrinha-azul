from pydantic import BaseModel
from datetime import datetime
from pydantic import BaseModel, validator

class ExecutionDate(BaseModel):
    execution_date: str

    @validator('execution_date')
    def validate_date_format(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d %H:%M')
        except ValueError:
            raise ValueError("Formato de data inválido. Use o formato 'YYYY-MM-DD HH:MM'.")

        return v