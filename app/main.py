# path: ./app/main.py

from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from . import crud
from . import models
from datetime import date
from .database import get_db, engine
from .schemas import TransactionCreate, TransactionResponse, BalanceInit
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Criação das tabelas do banco de dados
models.Base.metadata.create_all(bind=engine)

@app.get("/current_balance/", response_model=float)
async def read_current_balance(db: Session = Depends(get_db)):
    """
    Retorna o saldo atual.
    """
    balance = await crud.get_current_balance(db)
    return balance

@app.post("/initialize_balance/", response_model=TransactionResponse)
async def initialize_balance(
    balance_init: BalanceInit,
    db: Session = Depends(get_db)
):
    """
    Define o saldo inicial se não houver transações existentes.
    """
    if db.query(models.Transaction).count() > 0:
        raise HTTPException(status_code=400, detail="Initial balance can only be set if no transactions exist.")
    
    initial_transaction = TransactionCreate(
        date=balance_init.date,
        amount=balance_init.amount,
        description="Initial balance"
    )
    return crud.add_transaction(db=db, transaction=initial_transaction)

@app.post("/transactions/", response_model=TransactionResponse)
async def add_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
):
    """
    Adiciona uma nova transação e atualiza o saldo.
    """
    return  crud.add_transaction(db=db, transaction=transaction)

@app.get("/transactions/", response_model=List[TransactionResponse])
async def read_transactions(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Retorna as transações dentro de um período especificado.
    """
    transactions = crud.get_transactions_by_period(db, start_date=start_date, end_date=end_date)
    return transactions

@app.post("/reset_balance/", status_code=204)
async def reset_balance(
    db: Session = Depends(get_db)
):
    """
    Reseta o saldo inicial, removendo todas as transações existentes.
    """
    await crud.delete_all_transactions(db)  # Esta função precisa ser implementada no módulo crud.
    return {"detail": "Balance reset successfully."}