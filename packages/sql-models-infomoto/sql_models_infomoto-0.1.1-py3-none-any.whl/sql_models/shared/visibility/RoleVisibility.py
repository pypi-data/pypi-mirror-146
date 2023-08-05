from sqlmodel import Field

from sql_models.shared.role.Role import Role


class RoleVisibility:
    visibility: Role | None = Field(default=False)


