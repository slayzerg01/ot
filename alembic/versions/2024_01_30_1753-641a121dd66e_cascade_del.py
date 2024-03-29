"""cascade del

Revision ID: 641a121dd66e
Revises: c307b531fd6a
Create Date: 2024-01-30 17:53:02.418365

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "641a121dd66e"
down_revision: Union[str, None] = "c307b531fd6a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, "certificates", ["id"])
    op.drop_constraint(
        "certificates_employee_id_fkey", "certificates", type_="foreignkey"
    )
    op.create_foreign_key(None, "certificates", "employees", ["employee_id"], ["id"])
    op.create_unique_constraint(None, "divisions", ["id"])
    op.create_unique_constraint(None, "employees", ["id"])
    op.drop_constraint("employees_position_id_fkey", "employees", type_="foreignkey")
    op.drop_constraint("employees_subdivision_id_fkey", "employees", type_="foreignkey")
    op.create_foreign_key(None, "employees", "positions", ["position_id"], ["id"])
    op.create_foreign_key(None, "employees", "subdivisions", ["subdivision_id"], ["id"])
    op.create_unique_constraint(None, "exams", ["id"])
    op.drop_constraint("exams_employee_id_fkey", "exams", type_="foreignkey")
    op.create_foreign_key(
        None, "exams", "employees", ["employee_id"], ["id"], ondelete="CASCADE"
    )
    op.create_unique_constraint(None, "examtypes", ["id"])
    op.create_unique_constraint(None, "positions", ["id"])
    op.create_unique_constraint(None, "subdivisions", ["id"])
    op.drop_constraint(
        "subdivisions_division_id_fkey", "subdivisions", type_="foreignkey"
    )
    op.create_foreign_key(None, "subdivisions", "divisions", ["division_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "subdivisions", type_="foreignkey")
    op.create_foreign_key(
        "subdivisions_division_id_fkey",
        "subdivisions",
        "divisions",
        ["division_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_constraint(None, "subdivisions", type_="unique")
    op.drop_constraint(None, "positions", type_="unique")
    op.drop_constraint(None, "examtypes", type_="unique")
    op.drop_constraint(None, "exams", type_="foreignkey")
    op.create_foreign_key(
        "exams_employee_id_fkey", "exams", "employees", ["employee_id"], ["id"]
    )
    op.drop_constraint(None, "exams", type_="unique")
    op.drop_constraint(None, "employees", type_="foreignkey")
    op.drop_constraint(None, "employees", type_="foreignkey")
    op.create_foreign_key(
        "employees_subdivision_id_fkey",
        "employees",
        "subdivisions",
        ["subdivision_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "employees_position_id_fkey",
        "employees",
        "positions",
        ["position_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_constraint(None, "employees", type_="unique")
    op.drop_constraint(None, "divisions", type_="unique")
    op.drop_constraint(None, "certificates", type_="foreignkey")
    op.create_foreign_key(
        "certificates_employee_id_fkey",
        "certificates",
        "employees",
        ["employee_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_constraint(None, "certificates", type_="unique")
    # ### end Alembic commands ###
