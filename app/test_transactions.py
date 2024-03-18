# path: ./app/test_transactions.py
import unittest
from datetime import date
from app.main import add_transaction
from app.schemas import TransactionCreate
from app.models import Transaction  # Importe o modelo Transaction para verificar o resultado
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base

class TestTransactions(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')  # Cria um banco de dados sqlite temporário para testes
        Base.metadata.create_all(self.engine)  # Cria todas as tabelas no banco de dados em memória
        self.connection = self.engine.connect()
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        # Use o esquema Pydantic para criar dados de exemplo para o teste
        self.transaction_data = TransactionCreate(
            date=date.today(),
            description="Test",
            amount=100.0
        )

    def test_add_transaction(self):
        # Crie uma sessão para interagir com o banco de dados
        db = self.SessionLocal()
        # Chame a função add_transaction passando um objeto Pydantic e a sessão do banco de dados
        add_transaction(transaction=self.transaction_data, db=db)
        db.commit()  # Confirme as alterações no banco de dados
        # Verifique se a transação foi adicionada corretamente
        result = db.query(Transaction).first()
        self.assertIsNotNone(result)  # Verifique se o resultado não é None
        self.assertEqual(result.description, self.transaction_data.description)
        self.assertEqual(result.amount, self.transaction_data.amount)
        db.close()  # Feche a sessão após usar

    def tearDown(self):
        self.connection.close()
        self.engine.dispose()  # Encerre a conexão com o banco de dados

if __name__ == '__main__':
    unittest.main()
