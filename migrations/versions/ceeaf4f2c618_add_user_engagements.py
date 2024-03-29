"""add user engagements

Revision ID: ceeaf4f2c618
Revises: c6acaa686593
Create Date: 2020-11-18 18:39:29.506872

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ceeaf4f2c618'
down_revision = 'c6acaa686593'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_engagements',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=100), nullable=True),
    sa.Column('weekday', sa.String(length=20), nullable=True),
    sa.Column('month', sa.String(length=20), nullable=True),
    sa.Column('day', sa.Integer(), nullable=True),
    sa.Column('time', sa.String(length=20), nullable=True),
    sa.Column('am_pm', sa.String(length=2), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_engagements')
    # ### end Alembic commands ###
