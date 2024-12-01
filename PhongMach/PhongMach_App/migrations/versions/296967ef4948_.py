"""empty message

Revision ID: 296967ef4948
Revises: dbb4c1bb4da4
Create Date: 2024-11-25 14:34:13.010276

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '296967ef4948'
down_revision = 'dbb4c1bb4da4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exam_schedule', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_book', sa.Boolean(), nullable=False))
        batch_op.drop_column('is_free')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exam_schedule', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_free', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
        batch_op.drop_column('is_book')

    # ### end Alembic commands ###