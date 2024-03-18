# path: ./app/crud.py

from sqlalchemy.orm import Session
from . import models
from .schemas import TransactionCreate
from datetime import date
from typing import Optional

def add_transaction(db: Session, transaction: TransactionCreate):
    # Busque a última transação para obter o saldo atual
    last_transaction = db.query(models.Transaction).order_by(models.Transaction.id.desc()).first()
    new_balance = (last_transaction.balance if last_transaction else 0) + transaction.amount
    
    # Crie a nova transação com o saldo atualizado
    db_transaction = models.Transaction(
        date=transaction.date,
        amount=transaction.amount,
        description=transaction.description,
        balance=new_balance  # Use o novo saldo calculado
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transactions_by_period(db: Session, start_date: Optional[date] = None, end_date: Optional[date] = None):
    query = db.query(models.Transaction)
    if start_date:
        query = query.filter(models.Transaction.date >= start_date)
    if end_date:
        query = query.filter(models.Transaction.date <= end_date)
    return query.all()


async def delete_all_transactions(db: Session):
    """
    Remove todas as transações do banco de dados.
    """
    try:
        # Remover todas as transações
        db.query(models.Transaction).delete()
        # Efetivar as mudanças no banco de dados
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
async def get_current_balance(db: Session):
    """
    Calcula e retorna o saldo atual com base no conjunto de transações.
    """
    transactions = db.query(models.Transaction).all()
    balance = sum(transaction.amount for transaction in transactions)
    return balance