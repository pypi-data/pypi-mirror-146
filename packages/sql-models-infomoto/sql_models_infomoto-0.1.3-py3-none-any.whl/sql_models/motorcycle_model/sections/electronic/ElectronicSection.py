from camel_model.CamelModel import CamelModel

from sql_models.motorcycle_model.sections.electronic.ElectronicElement import ElectronicElement


class ElectronicSection(CamelModel):
    elements: list[ElectronicElement] | None
