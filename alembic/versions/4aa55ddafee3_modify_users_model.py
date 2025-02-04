"""Modify Users model

Revision ID: 4aa55ddafee3
Revises: 
Create Date: 2025-02-03 10:48:31.853755

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4aa55ddafee3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Example of adding a column
    op.add_column('users', sa.Column('is_active', sa.Boolean(), server_default=sa.text('true')))
   

def downgrade() -> None:
    # Example of removing the added columns
    op.drop_column('users', 'is_active')
    

