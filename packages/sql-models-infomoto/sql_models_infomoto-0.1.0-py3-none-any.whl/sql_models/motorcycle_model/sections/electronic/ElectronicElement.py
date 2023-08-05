from camel_model.CamelModel import CamelModel

from sql_models.motorcycle_model.sections.electronic.ElectronicElementComponent import ElectronicElementComponent


class ElectronicElement(CamelModel):
    name: str | None
    components: list[ElectronicElementComponent]