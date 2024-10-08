"""empty message

Revision ID: f1c869d78699
Revises: 
Create Date: 2020-06-19 10:32:05.623872

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1c869d78699'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    # op.create_table('users',
    # sa.Column('id', sa.Integer(), nullable=False),
    # sa.Column('number', sa.String(length=20), nullable=False),
    # sa.Column('number_2', sa.String(length=20), nullable=True),
    # sa.Column('registered', sa.Integer(), nullable=True),
    # sa.Column('last_month_completed', sa.Integer(), nullable=False),
    # sa.Column('airtime_number', sa.String(length=20), nullable=False),
    # sa.PrimaryKeyConstraint('id'),
    # )
    #
    #
    # op.create_table("baseline_questions",
    # sa.Column('id', sa.Integer(), nullable=False),
    # sa.Column('content', sa.String(length=1600), nullable=False),
    # sa.Column('num_ops', sa.Integer, nullable=False),
    # sa.PrimaryKeyConstraint('id'),
    # ),
    #
    # op.create_table("baseline_answers",
    # sa.Column('id', sa.Integer(), nullable=False),
    # sa.Column('content', sa.String(length=1600), nullable=False),
    # sa.Column('question_id', sa.Integer(), nullable=False),
    # sa.Column('user_id', sa.Integer(), nullable=False),
    # sa.ForeignKeyConstraint(['question_id'], ['baseline_questions.id']),
    # sa.ForeignKeyConstraint(['user_id'], ['users.id']),
    # sa.PrimaryKeyConstraint('id'),
    # ),
    #
    op.create_table("monthly_questions",
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(length=1600), nullable=False),
    sa.Column('num_ops', sa.Integer, nullable=False),
    sa.PrimaryKeyConstraint('id'),
    ),

    op.create_table("monthly_answers",
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(length=1600), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('month', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['monthly_questions.id']),
    sa.ForeignKeyConstraint(['user_id'], ['users.id']),
    sa.PrimaryKeyConstraint('id'),
    ),

    # op.create_table("responses",
    # sa.Column('id', sa.Integer(), nullable=False),
    # sa.Column('number', sa.String(length=20), nullable=False),
    # sa.Column('month', sa.Integer(), nullable = False),
    # sa.Column('question_1', sa.Integer(), nullable=False),
    # sa.Column('question_2', sa.Integer(), nullable=False),
    # sa.Column('question_3', sa.Integer(), nullable=False),
    # sa.Column('date_completed', sa.DateTime(), nullable=True),
    # sa.PrimaryKeyConstraint('id'),
    # )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###


    # op.drop_table('baseline_answers')
    # op.drop_table('baseline_questions')
    op.drop_table('monthly_answers')
    op.drop_table('monthly_questions')
    # op.drop_table('users')
    # op.drop_table('responses')
    # ### end Alembic commands ###
