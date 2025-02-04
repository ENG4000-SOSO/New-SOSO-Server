"""Set default value for role column

Revision ID: 7ce8303e71b3
Revises: 4aa55ddafee3
Create Date: 2025-02-03 11:23:44.793271

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ce8303e71b3'
down_revision: Union[str, None] = '4aa55ddafee3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column('users', 'role', 
        existing_type=sa.Enum('admin', 'operator', 'viewer', name='user_roles'),
        server_default='viewer'
    )

def downgrade():
    op.alter_column('users', 'role', 
        existing_type=sa.Enum('admin', 'operator', 'viewer', name='user_roles'),
        server_default=None
    )

