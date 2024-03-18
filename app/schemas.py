#path: ./app/schemas.py

from pydantic import BaseModel
from datetime import date


# Modelo Pydantic para inicializar o saldo
class BalanceInit(BaseModel):
    date: date
    amount: float

# Modelo Pydantic para a entrada de dados da transação
class TransactionCreate(BaseModel):
    date: date
    description: str
    amount: float

# Modelo Pydantic para a resposta da transação
class TransactionResponse(BaseModel):
    id: int
    date: date
    description: str
    amount: float
    balance: float  # Adicione este campo para mostrar o saldo atualizado

    class Config:
        from_attributes = True  