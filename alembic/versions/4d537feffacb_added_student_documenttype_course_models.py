"""Added Student, DocumentType & Course models

Revision ID: 4d537feffacb
Revises: aeedebcd6b11
Create Date: 2017-03-19 13:04:47.697460

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4d537feffacb'
down_revision = 'aeedebcd6b11'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('courses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=100), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('updated_on', sa.DateTime(), nullable=False),
    sa.Column('erased', sa.Boolean(), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('semester', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=3), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_courses_code'), 'courses', ['code'], unique=False)
    op.create_index(op.f('ix_courses_description'), 'courses', ['description'], unique=False)
    op.create_index(op.f('ix_courses_id'), 'courses', ['id'], unique=False)
    op.create_table('document_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=100), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('updated_on', sa.DateTime(), nullable=False),
    sa.Column('erased', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_document_types_description'), 'document_types', ['description'], unique=False)
    op.create_index(op.f('ix_document_types_id'), 'document_types', ['id'], unique=False)
    op.create_table('students',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('updated_on', sa.DateTime(), nullable=False),
    sa.Column('erased', sa.Boolean(), nullable=False),
    sa.Column('first_name', sa.String(length=128), nullable=False),
    sa.Column('last_name', sa.String(length=128), nullable=False),
    sa.Column('doc_type_id', sa.Integer(), nullable=True),
    sa.Column('doc_number', sa.String(length=16), nullable=False),
    sa.Column('email', sa.String(length=256), nullable=False),
    sa.ForeignKeyConstraint(['doc_type_id'], ['document_types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_students_doc_number'), 'students', ['doc_number'], unique=False)
    op.create_index(op.f('ix_students_email'), 'students', ['email'], unique=False)
    op.create_index(op.f('ix_students_id'), 'students', ['id'], unique=False)
    op.create_index(op.f('ix_students_last_name'), 'students', ['last_name'], unique=False)
    op.drop_table('tests2')
    op.drop_table('tests3')
    op.drop_table('tests')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tests',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('description', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('created_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('updated_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('erased', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='tests_pkey')
    )
    op.create_table('tests3',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('description', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('created_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('updated_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('erased', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('another_column', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='tests3_pkey')
    )
    op.create_table('tests2',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('description', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('created_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('updated_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('erased', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='tests2_pkey')
    )
    op.drop_index(op.f('ix_students_last_name'), table_name='students')
    op.drop_index(op.f('ix_students_id'), table_name='students')
    op.drop_index(op.f('ix_students_email'), table_name='students')
    op.drop_index(op.f('ix_students_doc_number'), table_name='students')
    op.drop_table('students')
    op.drop_index(op.f('ix_document_types_id'), table_name='document_types')
    op.drop_index(op.f('ix_document_types_description'), table_name='document_types')
    op.drop_table('document_types')
    op.drop_index(op.f('ix_courses_id'), table_name='courses')
    op.drop_index(op.f('ix_courses_description'), table_name='courses')
    op.drop_index(op.f('ix_courses_code'), table_name='courses')
    op.drop_table('courses')
    # ### end Alembic commands ###
