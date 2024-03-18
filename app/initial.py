# path: ./alembic/versions/initial.py

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'transactions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('date', sa.Date, index=True),
        sa.Column('amount', sa.Float),
        sa.Column('description', sa.String)
    )

def downgrade():
    op.drop_table('transactions')

