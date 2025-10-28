"""Add priority and tags for task filtering

Revision ID: 5699622a4603
Revises: 1934c2ec8b3d
Create Date: 2025-10-28 00:17:23.761953

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5699622a4603'
down_revision = '1934c2ec8b3d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create priority enum type
    priority_enum = postgresql.ENUM('low', 'medium', 'high', 'urgent', name='priorityenum')
    priority_enum.create(op.get_bind())

    # Add new columns to task table
    op.add_column('task', sa.Column('priority', priority_enum, nullable=False, server_default='medium'))
    op.add_column('task', sa.Column('tags', postgresql.ARRAY(sa.String()), nullable=True, server_default='{}'))
    op.add_column('task', sa.Column('completeddate', sa.DateTime(), nullable=True))

    # Create indexes for filtering performance
    op.create_index('idx_tasks_status_priority', 'task', ['status', 'priority'])
    op.create_index('idx_tasks_due_date', 'task', ['dueDate'], unique=False)
    op.create_index('idx_tasks_created_date', 'task', ['createdDate'])
    op.create_index('idx_tasks_tags', 'task', ['tags'], unique=False, postgresql_using='gin')


def downgrade() -> None:
    # Drop indexes
    op.drop_index('idx_tasks_tags', 'task')
    op.drop_index('idx_tasks_created_date', 'task')
    op.drop_index('idx_tasks_due_date', 'task')
    op.drop_index('idx_tasks_status_priority', 'task')

    # Drop columns
    op.drop_column('task', 'completedDate')
    op.drop_column('task', 'tags')
    op.drop_column('task', 'priority')

    # Drop enum
    priority_enum = postgresql.ENUM('low', 'medium', 'high', 'urgent', name='priorityenum')
    priority_enum.drop(op.get_bind())
