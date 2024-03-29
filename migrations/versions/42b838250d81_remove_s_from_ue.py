"""remove s from ue

Revision ID: 42b838250d81
Revises: ceeaf4f2c618
Create Date: 2020-11-18 18:42:55.436288

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '42b838250d81'
down_revision = 'ceeaf4f2c618'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_engagement',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=100), nullable=True),
    sa.Column('weekday', sa.String(length=20), nullable=True),
    sa.Column('month', sa.String(length=20), nullable=True),
    sa.Column('day', sa.Integer(), nullable=True),
    sa.Column('time', sa.String(length=20), nullable=True),
    sa.Column('am_pm', sa.String(length=2), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('user_engagements')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_engagements',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('description', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('weekday', mysql.VARCHAR(length=20), nullable=True),
    sa.Column('month', mysql.VARCHAR(length=20), nullable=True),
    sa.Column('day', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('time', mysql.VARCHAR(length=20), nullable=True),
    sa.Column('am_pm', mysql.VARCHAR(length=2), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    op.drop_table('user_engagement')
    # ### end Alembic commands ###
