"""remove ufp fk

Revision ID: 8468c476f3ae
Revises: 762217bc1b0d
Create Date: 2020-11-18 19:13:00.581946

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8468c476f3ae'
down_revision = '762217bc1b0d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_friend_pairs_ibfk_2', 'user_friend_pairs', type_='foreignkey')
    op.drop_constraint('user_friend_pairs_ibfk_1', 'user_friend_pairs', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('user_friend_pairs_ibfk_1', 'user_friend_pairs', 'user', ['first_user'], ['id'])
    op.create_foreign_key('user_friend_pairs_ibfk_2', 'user_friend_pairs', 'user', ['second_user'], ['id'])
    # ### end Alembic commands ###
