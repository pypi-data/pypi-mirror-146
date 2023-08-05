from camel_model.CamelModel import CamelModel


class PowerSupplyComponentAttribute(CamelModel):
    name: str | None
    value: str | None
    observations: str | None
