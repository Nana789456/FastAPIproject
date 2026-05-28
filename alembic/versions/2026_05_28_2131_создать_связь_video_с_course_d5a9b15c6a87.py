"""создать связь Video с Course

Revision ID: d5a9b15c6a87
Revises: 0f138e0417f7
Create Date: 2026-05-28 21:31:50.001230

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5a9b15c6a87'
down_revision: Union[str, Sequence[str], None] = '0f138e0417f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('video') as batch_op:
        batch_op.add_column(sa.Column('course_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key('fk_video_course_id', 'course', ['course_id'], ['id'])

def downgrade() -> None:
    with op.batch_alter_table('video') as batch_op:
        batch_op.drop_constraint('fk_video_course_id', type_='foreignkey')
        batch_op.drop_column('course_id')
