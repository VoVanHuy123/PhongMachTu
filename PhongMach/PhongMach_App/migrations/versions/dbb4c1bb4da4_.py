"""empty message

Revision ID: dbb4c1bb4da4
Revises: 02ec754b693a
Create Date: 2024-11-25 14:01:25.519227

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dbb4c1bb4da4'
down_revision = '02ec754b693a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exam_registration', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_waiting', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exam_registration', schema=None) as batch_op:
        batch_op.drop_column('is_waiting')

    # ### end Alembic commands ###