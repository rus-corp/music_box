"""client_profile_table

Revision ID: baeea5030d7f
Revises: b71c5d2091be
Create Date: 2024-07-10 11:35:10.122005

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'baeea5030d7f'
down_revision: Union[str, None] = 'b71c5d2091be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('client_profile',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=False),
    sa.Column('certificate', sa.String(), nullable=False),
    sa.Column('contract_number', sa.String(), nullable=True),
    sa.Column('contract_date', sa.DateTime(), nullable=True),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('client', 'address')
    op.drop_column('client', 'contract_date')
    op.drop_column('client', 'contract_number')
    op.drop_column('client', 'certificate')
    op.drop_column('client', 'full_name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('client', sa.Column('full_name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('client', sa.Column('certificate', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('client', sa.Column('contract_number', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('client', sa.Column('contract_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('client', sa.Column('address', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_table('client_profile')
    # ### end Alembic commands ###