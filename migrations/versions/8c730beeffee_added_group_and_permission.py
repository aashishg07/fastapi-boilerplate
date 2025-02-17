"""added group and permission

Revision ID: 8c730beeffee
Revises: 55c98ba9fc73
Create Date: 2024-11-21 11:32:12.843329

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c730beeffee'
down_revision: Union[str, None] = '55c98ba9fc73'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('permission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('group', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group'], ['role.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('user', sa.Column('role', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user', 'role', ['role'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'role')
    op.drop_table('permission')
    op.drop_table('role')
    # ### end Alembic commands ###
