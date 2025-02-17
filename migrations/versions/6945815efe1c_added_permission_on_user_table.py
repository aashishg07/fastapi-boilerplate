"""added permission on user table

Revision ID: 6945815efe1c
Revises: 0560072843f5
Create Date: 2024-11-25 04:25:07.067398

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6945815efe1c'
down_revision: Union[str, None] = '0560072843f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_permission_fkey', 'user', type_='foreignkey')
    op.drop_column('user', 'permission')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('permission', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('user_permission_fkey', 'user', 'permission', ['permission'], ['id'])
    # ### end Alembic commands ###
