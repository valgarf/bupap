"""index

Revision ID: 04ead4e30266
Revises: 930a51864adb
Create Date: 2023-11-25 17:13:52.722781

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "04ead4e30266"
down_revision = "930a51864adb"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index("project_id", "Task", ["task_state", "order_id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("project_id", table_name="Task")
    # ### end Alembic commands ###