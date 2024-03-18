# path: ./app/models.py

from sqlalchemy import Column, Integer, String, Date, Float
from app.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    amount = Column(Float)
    description = Column(String)
    balance = Column(Float)  # Adicione este campo para manter o saldo corrente

