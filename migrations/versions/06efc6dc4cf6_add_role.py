"""add role

Revision ID: 06efc6dc4cf6
Revises: a505d63c7b7f
Create Date: 2019-10-05 22:31:03.490906

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06efc6dc4cf6'
down_revision = 'a505d63c7b7f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('role', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'role')
    # ### end Alembic commands ###
