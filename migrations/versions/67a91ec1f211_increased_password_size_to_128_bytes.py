"""Increased password size to 128 bytes

Revision ID: 67a91ec1f211
Revises: e9f64f096038
Create Date: 2022-12-07 20:19:35.404541

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67a91ec1f211'
down_revision = 'e9f64f096038'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(length=30),
               type_=sa.String(length=128),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'password',
               existing_type=sa.String(length=128),
               type_=sa.VARCHAR(length=30),
               existing_nullable=True)
    # ### end Alembic commands ###
