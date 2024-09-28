"""Add results stuff

Revision ID: 6614910ad05f
Revises: 
Create Date: 2024-09-19 19:24:04.301144

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6614910ad05f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('copy_paste_event', schema=None) as batch_op:
        batch_op.add_column(sa.Column('debate_id', sa.String(), nullable=False))
        batch_op.create_foreign_key('fk_copy_paste_event_debate_id', 'debate', ['debate_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('copy_paste_event', schema=None) as batch_op:
        batch_op.drop_constraint('fk_copy_paste_event_debate_id', type_='foreignkey')
        batch_op.drop_column('debate_id')

    # ### end Alembic commands ###