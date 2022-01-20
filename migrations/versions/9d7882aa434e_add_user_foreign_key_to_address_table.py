"""add user foreign key to address table

Revision ID: 9d7882aa434e
Revises: 76d65fcd8418
Create Date: 2022-01-20 15:19:29.031164

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d7882aa434e'
down_revision = '76d65fcd8418'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('phonebook', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'phonebook', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'phonebook', type_='foreignkey')
    op.drop_column('phonebook', 'user_id')
    # ### end Alembic commands ###
