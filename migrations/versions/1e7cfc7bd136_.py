"""empty message

Revision ID: 1e7cfc7bd136
Revises: 7a5f563ea849
Create Date: 2021-01-01 11:32:39.668305

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1e7cfc7bd136'
down_revision = '7a5f563ea849'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('group_engagement', 'day')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('group_engagement', sa.Column('day', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
