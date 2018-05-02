"""initial database

Revision ID: 658f1627f050
Revises: 
Create Date: 2018-05-02 15:29:05.280833

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '658f1627f050'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('joined', sa.DateTime(), nullable=False),
    sa.Column('actual_name', sa.String(length=128), nullable=True),
    sa.Column('favourite_styles', sa.String(length=128), nullable=True),
    sa.Column('about', sa.String(length=2048), nullable=True),
    sa.Column('contact', sa.String(length=128), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('activity',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('description', sa.String(length=256), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('recipe',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('style', sa.String(length=128), nullable=True),
    sa.Column('ingredients', sa.String(length=2048), nullable=True),
    sa.Column('method', sa.String(length=8192), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('brew',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('brewed_on', sa.DateTime(), nullable=False),
    sa.Column('description', sa.String(length=8192), nullable=True),
    sa.Column('recipe_id', sa.Integer(), nullable=True),
    sa.Column('brewer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['brewer_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tasting',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tasted_on', sa.DateTime(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('comment', sa.String(length=4096), nullable=True),
    sa.Column('recipe_id', sa.Integer(), nullable=True),
    sa.Column('brew_id', sa.Integer(), nullable=True),
    sa.Column('taster_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['brew_id'], ['brew.id'], ),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id'], ),
    sa.ForeignKeyConstraint(['taster_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tasting')
    op.drop_table('brew')
    op.drop_table('recipe')
    op.drop_table('activity')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
