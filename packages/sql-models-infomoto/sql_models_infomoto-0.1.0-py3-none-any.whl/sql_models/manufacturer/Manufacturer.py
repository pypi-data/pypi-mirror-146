from sqlmodel import Field

from sql_models.SQLCamelModel import SQLCamelModel
from sql_models.manufacturer.NewManufacturer import NewManufacturer
from sql_models.shared.visibility.RoleVisibility import RoleVisibility


class ManufacturerEntity(RoleVisibility, SQLCamelModel, table=True):
    __tablename__ = 'manufacturer'

    id: str = Field(
        primary_key=True,
        # max_length=32,
    )
    image_width: int | None
    image_height: int | None

    def __init__(
            self,
            **data,
    ):
        super().__init__(**data)

    @classmethod
    def from_new_manufacturer(cls, new_manufacturer: NewManufacturer):
        manufacturer = cls(
            **(new_manufacturer.dict()),
        )

        manufacturer.id = manufacturer.name.replace(" ", "-").lower()
        manufacturer.name = manufacturer.name.title()

        return manufacturer
