"""empty message

Revision ID: ed2bf7b9c631
Revises: 9a417b79de83
Create Date: 2020-12-30 20:06:47.350037

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed2bf7b9c631'
down_revision = '9a417b79de83'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('friend_request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender', sa.Integer(), nullable=True),
    sa.Column('receiver', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['receiver'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('friend_request')
    # ### end Alembic commands ###
