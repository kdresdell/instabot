"""start

Revision ID: e4854d160634
Revises: 
Create Date: 2021-03-08 18:54:14.006363

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4854d160634'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bots',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('insta_user', sa.String(length=20), nullable=True),
    sa.Column('insta_password', sa.String(length=20), nullable=True),
    sa.Column('img_data', sa.LargeBinary(), nullable=True),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.Column('followers', sa.Integer(), nullable=True),
    sa.Column('followees', sa.Integer(), nullable=True),
    sa.Column('posts', sa.Integer(), nullable=True),
    sa.Column('tags', sa.Text(), nullable=True),
    sa.Column('comments', sa.Text(), nullable=True),
    sa.Column('location', sa.String(length=20), nullable=True),
    sa.Column('radius', sa.Integer(), nullable=True),
    sa.Column('media', sa.String(length=20), nullable=True),
    sa.Column('created_dt', sa.DateTime(), nullable=True),
    sa.Column('paid', sa.Boolean(), nullable=True),
    sa.Column('status', sa.Text(), nullable=True),
    sa.Column('end_dt', sa.DateTime(), nullable=True),
    sa.Column('results', sa.JSON(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_info')
    op.drop_table('bots')
    # ### end Alembic commands ###