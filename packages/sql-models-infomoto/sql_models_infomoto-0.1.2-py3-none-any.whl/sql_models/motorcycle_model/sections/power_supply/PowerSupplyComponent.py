from camel_model.CamelModel import CamelModel

from sql_models.motorcycle_model.sections.power_supply.PowerSupplyComponentAttribute import \
    PowerSupplyComponentAttribute


class PowerSupplyComponent(CamelModel):
    name: str
    value: str | None
    observations: str | None
    attributes: list[PowerSupplyComponentAttribute] | None
