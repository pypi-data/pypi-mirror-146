from sqlmodel import Field

from sql_models.SQLCamelModel import SQLCamelModel
from sql_models.shared.role.Role import Role


class RoleVisibility(SQLCamelModel):
    visibility: Role | None = Field(default=False)


