"""added permission on user table

Revision ID: f2d7cdd236e9
Revises: 6945815efe1c
Create Date: 2024-11-25 04:32:33.381311

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f2d7cdd236e9'
down_revision: Union[str, None] = '6945815efe1c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('permission_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user', 'permission', ['permission_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'permission_id')
    # ### end Alembic commands ###
