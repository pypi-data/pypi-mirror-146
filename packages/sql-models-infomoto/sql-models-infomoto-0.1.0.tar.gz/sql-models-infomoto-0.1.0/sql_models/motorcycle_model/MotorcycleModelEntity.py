from sqlalchemy import Column, JSON
from sqlmodel import Field

from sql_models.SQLCamelModel import SQLCamelModel

from sql_models.shared.visibility.RoleVisibility import RoleVisibility

from sql_models.motorcycle_model.MotorcycleModel import MotorcycleModel


class MotorcycleModelEntity(RoleVisibility, SQLCamelModel, table=True):
    __tablename__ = 'models'

    id: str = Field(
        primary_key=True,
        # max_length=32,
    )

    manufacturer_id: str = Field(
        primary_key=True,
        foreign_key='manufacturer.id',
        # max_length=32,
    )

    model_info: MotorcycleModel | None = Field(
        default=None,
        sa_column=Column(JSON),
    )

