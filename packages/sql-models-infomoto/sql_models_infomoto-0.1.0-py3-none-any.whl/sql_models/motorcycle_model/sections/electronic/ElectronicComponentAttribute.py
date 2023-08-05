from camel_model.CamelModel import CamelModel


class ElectronicComponentAttribute(CamelModel):
    name: str | None
    value: str | None
    observations: str | None