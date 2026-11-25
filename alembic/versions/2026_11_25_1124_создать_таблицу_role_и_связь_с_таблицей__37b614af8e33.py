"""создать таблицу role и связь с таблицей user

Revision ID: 37b614af8e33
Revises: 7c1e4a9b2f30
Create Date: 2026-11-25 11:24:34.779058

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37b614af8e33'
down_revision: Union[str, Sequence[str], None] = '7c1e4a9b2f30'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # 1. Создаём таблицу ролей.
    role_table = op.create_table(
        'role',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=20), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name', name='uq_role_name')
    )

    # 2. Создаём базовую роль user.
    op.bulk_insert(
        role_table,
        [
            {
                'name': 'user',
                'description': 'Пользователь'
            }
        ]
    )

    # 3. Добавляем поле role_id с временным разрешением NULL.
    op.add_column(
        'user',
        sa.Column('role_id', sa.Integer(), nullable=True)
    )

    # 4. Присваиваем существующим пользователям роль user.
    op.execute("""
        UPDATE "user"
        SET role_id = (
            SELECT id FROM role WHERE name = 'user'
        )
    """)

    # 5. Запрещаем NULL и создаём внешний ключ.
    with op.batch_alter_table('user') as batch_op:
        batch_op.alter_column(
            'role_id',
            existing_type=sa.Integer(),
            nullable=False
        )
        batch_op.create_foreign_key(
            'fk_user_role_id',
            'role',
            ['role_id'],
            ['id']
        )


def downgrade() -> None:
    """Downgrade schema."""

    # 1. Удаляем внешний ключ и поле role_id.
    with op.batch_alter_table('user') as batch_op:
        batch_op.drop_constraint(
            'fk_user_role_id',
            type_='foreignkey'
        )
        batch_op.drop_column('role_id')

    # 2. Удаляем таблицу ролей.
    op.drop_table('role')