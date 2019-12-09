"""add tower_mode_1 to Task

Revision ID: f4c9dd3413ed
Revises: 464ee5e1d2aa
Create Date: 2019-12-07 16:48:51.157241

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4c9dd3413ed'
down_revision = '464ee5e1d2aa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('tower_mode_1', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task', 'tower_mode_1')
    # ### end Alembic commands ###