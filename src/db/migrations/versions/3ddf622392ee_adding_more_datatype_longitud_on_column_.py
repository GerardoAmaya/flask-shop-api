"""Adding more datatype longitud on column password user table

Revision ID: 3ddf622392ee
Revises: e88409a8e6a5
Create Date: 2024-09-05 15:26:49.047908

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3ddf622392ee'
down_revision = 'e88409a8e6a5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=mysql.VARCHAR(length=128),
               type_=sa.String(length=350),
               existing_comment='The hashed password of the user.',
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.String(length=350),
               type_=mysql.VARCHAR(length=128),
               existing_comment='The hashed password of the user.',
               existing_nullable=False)

    # ### end Alembic commands ###