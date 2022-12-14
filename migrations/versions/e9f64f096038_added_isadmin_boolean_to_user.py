"""Added isAdmin boolean to User

Revision ID: e9f64f096038
Revises: 7ea8869c1114
Create Date: 2022-12-07 20:00:45.280731

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9f64f096038'
down_revision = '7ea8869c1114'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('isAdmin', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'isAdmin')
    # ### end Alembic commands ###
