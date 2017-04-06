"""Adding mailman list to course

Revision ID: a4834d6b5427
Revises: b63e6c512eaa
Create Date: 2017-04-06 12:03:59.031979

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4834d6b5427'
down_revision = 'b63e6c512eaa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('courses', sa.Column('list_name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('courses', 'list_name')
    # ### end Alembic commands ###
