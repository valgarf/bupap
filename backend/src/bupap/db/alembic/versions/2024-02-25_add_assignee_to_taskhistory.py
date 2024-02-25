"""
add 'assignee' to TaskHistory

Revision ID: 5cce5ba026f2
Revises: 04ead4e30266
Create Date: 2024-02-25 10:45:47.456628

"""
# third-party
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "5cce5ba026f2"
down_revision = "04ead4e30266"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("TaskHistory") as batch_op:
        batch_op.add_column(sa.Column("assignee_id", sa.Integer(), nullable=True))
        batch_op.create_index(op.f("ix_TaskHistory_assignee_id"), ["assignee_id"], unique=False)
        batch_op.create_foreign_key(
            op.f("fk_TaskHistroy_assignee_id_User"), "User", ["assignee_id"], ["id"]
        )


def downgrade() -> None:
    with op.batch_alter_table("TaskHistory") as batch_op:
        # batch_op.drop_constraint(op.f("fk_TaskHistroy_assignee_id_User"), type_="foreignkey")
        batch_op.drop_index(op.f("ix_TaskHistory_assignee_id"))
        batch_op.drop_column("assignee_id")
