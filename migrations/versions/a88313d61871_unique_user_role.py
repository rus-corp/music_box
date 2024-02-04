"""unique user role

Revision ID: a88313d61871
Revises: b33d9968be0f
Create Date: 2024-02-04 14:58:43.635364

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a88313d61871'
down_revision: Union[str, None] = 'b33d9968be0f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'user_role', ['role_name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_role', type_='unique')
    # ### end Alembic commands ###
