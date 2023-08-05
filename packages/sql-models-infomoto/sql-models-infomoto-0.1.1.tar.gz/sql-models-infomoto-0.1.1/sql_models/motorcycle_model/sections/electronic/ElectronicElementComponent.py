from camel_model.CamelModel import CamelModel

from sql_models.motorcycle_model.sections.electronic.ElectronicComponentAttribute import ElectronicComponentAttribute


class ElectronicElementComponent(CamelModel):
    name: str | None
    value: str | None
    observations: str | None
    attributes: list[ElectronicComponentAttribute] | None
