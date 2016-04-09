"""initial migration

Revision ID: 1353e9b4cccd
Revises: None
Create Date: 2016-01-13 21:29:33.432330

"""

# revision identifiers, used by Alembic.
revision = '1353e9b4cccd'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ship',
    sa.Column('famliy_id', sa.Integer(), nullable=False),
    sa.Column('doctor_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctor.id'], ),
    sa.ForeignKeyConstraint(['famliy_id'], ['famliy.id'], ),
    sa.PrimaryKeyConstraint('famliy_id', 'doctor_id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ship')
    ### end Alembic commands ###