"""empty message

Revision ID: a7d362527749
Revises: ff6d51c2def3
Create Date: 2020-11-19 09:58:15.636349

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a7d362527749'
down_revision = 'ff6d51c2def3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_friend_pairs')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_friend_pairs',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('first_user', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('second_user', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['first_user'], ['user.id'], name='user_friend_pairs_ibfk_2'),
    sa.ForeignKeyConstraint(['second_user'], ['user.id'], name='user_friend_pairs_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
