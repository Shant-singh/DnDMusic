"""empty message

Revision ID: 57936b9b013a
Revises: 8fbe0c04351d
Create Date: 2021-10-03 15:10:21.836923

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57936b9b013a'
down_revision = '8fbe0c04351d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('EntityInstance', sa.Column('hash', sa.String(length=10), nullable=True))
    op.add_column('MapInstance', sa.Column('hash', sa.String(length=10), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('MapInstance', 'hash')
    op.drop_column('EntityInstance', 'hash')
    # ### end Alembic commands ###
