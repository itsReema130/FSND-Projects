"""empty message

Revision ID: 85a2cdead765
Revises: 845ec2bdb06f
Create Date: 2021-06-23 22:54:52.210302

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '85a2cdead765'
down_revision = '845ec2bdb06f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('artist', 'genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('venue', 'genres',
               existing_type=postgresql.ARRAY(sa.VARCHAR(length=120)),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venue', 'genres',
               existing_type=postgresql.ARRAY(sa.VARCHAR(length=120)),
               nullable=False)
    op.alter_column('artist', 'genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    # ### end Alembic commands ###
