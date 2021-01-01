"""empty message

Revision ID: 3fb0e74330b1
Revises: 9b5db88b7e71
Create Date: 2020-11-19 17:07:12.910550

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3fb0e74330b1'
down_revision = '9b5db88b7e71'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('group_members', sa.Column('groupt_id', sa.Integer(), nullable=True))
    op.add_column('group_members', sa.Column('usert_id', sa.Integer(), nullable=True))
    op.drop_constraint('group_members_ibfk_2', 'group_members', type_='foreignkey')
    op.drop_constraint('group_members_ibfk_1', 'group_members', type_='foreignkey')
    op.create_foreign_key(None, 'group_members', 'user_group', ['groupt_id'], ['id'])
    op.create_foreign_key(None, 'group_members', 'user', ['usert_id'], ['id'])
    op.drop_column('group_members', 'group_id')
    op.drop_column('group_members', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('group_members', sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('group_members', sa.Column('group_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'group_members', type_='foreignkey')
    op.drop_constraint(None, 'group_members', type_='foreignkey')
    op.create_foreign_key('group_members_ibfk_1', 'group_members', 'user_group', ['group_id'], ['id'])
    op.create_foreign_key('group_members_ibfk_2', 'group_members', 'user', ['user_id'], ['id'])
    op.drop_column('group_members', 'usert_id')
    op.drop_column('group_members', 'groupt_id')
    # ### end Alembic commands ###