"""

Revision ID: 022dd4987a25
Revises: 341896cf4629
Create Date: 2024-04-20 13:28:39.711825

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '022dd4987a25'
down_revision: Union[str, None] = '341896cf4629'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('client_group', sa.Column('client_cluster_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'client_group', 'client_cluster', ['client_cluster_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'client_group', type_='foreignkey')
    op.drop_column('client_group', 'client_cluster_id')
    # ### end Alembic commands ###
