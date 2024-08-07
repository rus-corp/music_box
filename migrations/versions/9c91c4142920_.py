"""

Revision ID: 9c91c4142920
Revises: f1ca38ce7584
Create Date: 2024-08-07 16:09:28.850060

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c91c4142920'
down_revision: Union[str, None] = 'f1ca38ce7584'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bases',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('base_collection',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('main_base_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['main_base_id'], ['bases.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trackCollection_baseCollection_association',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('trac_collection_id', sa.Integer(), nullable=True),
    sa.Column('base_collection_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['base_collection_id'], ['base_collection.id'], ),
    sa.ForeignKeyConstraint(['trac_collection_id'], ['track_collection.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('promo_audio',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('file_path', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('promo_audio')
    op.drop_table('trackCollection_baseCollection_association')
    op.drop_table('base_collection')
    op.drop_table('bases')
    # ### end Alembic commands ###
