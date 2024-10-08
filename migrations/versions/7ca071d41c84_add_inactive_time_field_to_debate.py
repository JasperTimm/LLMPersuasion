"""Add inactive_time field to Debate

Revision ID: 7ca071d41c84
Revises: a69caa636752
Create Date: 2024-10-04 16:07:28.686724

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ca071d41c84'
down_revision = 'a69caa636752'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('debate', schema=None) as batch_op:
        batch_op.add_column(sa.Column('inactive_time', sa.Integer(), nullable=False, server_default='0'))
        
    # Set inactive_time to 0 for existing records
    op.execute('UPDATE debate SET inactive_time = 0 WHERE inactive_time IS NULL')
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('debate', schema=None) as batch_op:
        batch_op.drop_column('inactive_time')

    # ### end Alembic commands ###
