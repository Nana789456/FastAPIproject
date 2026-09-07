"""rename password to hashed_password

Revision ID: 28892abb0c18
Revises: 2530be6e9ed2
Create Date: 2026-09-07 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28892abb0c18'
down_revision: Union[str, Sequence[str], None] = '2530be6e9ed2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('user') as batch_op:
        batch_op.alter_column(
            'password',
            new_column_name='hashed_password',
            existing_type=sa.String(length=30),
            type_=sa.String(length=255),
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('user') as batch_op:
        batch_op.alter_column(
            'hashed_password',
            new_column_name='password',
            existing_type=sa.String(length=255),
            type_=sa.String(length=30),
        )
