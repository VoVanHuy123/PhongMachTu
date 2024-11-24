"""Tạo các bảng cơ bản

Revision ID: c4a2fb0b5c4b
Revises: 
Create Date: 2024-11-21 11:50:49.587393

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4a2fb0b5c4b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=50), nullable=False),
    sa.Column('create_day', sa.Date(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('password'),
    sa.UniqueConstraint('user_name')
    )
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('exam_time',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.Time(), nullable=False),
    sa.Column('end_time', sa.Time(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('medicine',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('inventory', sa.Float(), nullable=False),
    sa.Column('unit_price', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('medicine_unit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('unit', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('med_category',
    sa.Column('medicine_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['medicine_id'], ['medicine.id'], ),
    sa.PrimaryKeyConstraint('medicine_id', 'category_id')
    )
    op.create_table('med_unit',
    sa.Column('medicine_id', sa.Integer(), nullable=False),
    sa.Column('unit_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['medicine_id'], ['medicine.id'], ),
    sa.ForeignKeyConstraint(['unit_id'], ['medicine_unit.id'], ),
    sa.PrimaryKeyConstraint('medicine_id', 'unit_id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('gender', sa.String(length=50), nullable=True),
    sa.Column('birth_day', sa.Date(), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('image', sa.String(length=255), nullable=True),
    sa.Column('account_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('doctor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('specialty', sa.String(length=100), nullable=True),
    sa.Column('experience', sa.String(length=100), nullable=True),
    sa.Column('current_workplace', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('nurse',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('patient',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('insurance_number', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('insurance_number')
    )
    op.create_table('phone_number',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.String(length=15), nullable=False),
    sa.Column('type_number', sa.String(length=50), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('number')
    )
    op.create_table('exam_registration',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('symptom', sa.String(length=255), nullable=True),
    sa.Column('exam_day', sa.Date(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('doctor_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctor.id'], ),
    sa.ForeignKeyConstraint(['patient_id'], ['patient.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('exam_schedule',
    sa.Column('exam_time_id', sa.Integer(), nullable=False),
    sa.Column('doctor_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctor.id'], ),
    sa.ForeignKeyConstraint(['exam_time_id'], ['exam_time.id'], ),
    sa.PrimaryKeyConstraint('exam_time_id', 'doctor_id')
    )
    op.create_table('medical_exam',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('diagnosis', sa.String(length=255), nullable=True),
    sa.Column('exam_day', sa.Date(), nullable=True),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('doctor_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctor.id'], ),
    sa.ForeignKeyConstraint(['patient_id'], ['patient.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('detail_exam',
    sa.Column('medical_exam_id', sa.Integer(), nullable=False),
    sa.Column('medicine_id', sa.Integer(), nullable=False),
    sa.Column('instruct', sa.String(length=255), nullable=True),
    sa.Column('quantity', sa.Float(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['medical_exam_id'], ['medical_exam.id'], ),
    sa.ForeignKeyConstraint(['medicine_id'], ['medicine.id'], ),
    sa.PrimaryKeyConstraint('medical_exam_id', 'medicine_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('detail_exam')
    op.drop_table('medical_exam')
    op.drop_table('exam_schedule')
    op.drop_table('exam_registration')
    op.drop_table('phone_number')
    op.drop_table('patient')
    op.drop_table('nurse')
    op.drop_table('doctor')
    op.drop_table('admin')
    op.drop_table('user')
    op.drop_table('med_unit')
    op.drop_table('med_category')
    op.drop_table('medicine_unit')
    op.drop_table('medicine')
    op.drop_table('exam_time')
    op.drop_table('category')
    op.drop_table('account')
    # ### end Alembic commands ###
