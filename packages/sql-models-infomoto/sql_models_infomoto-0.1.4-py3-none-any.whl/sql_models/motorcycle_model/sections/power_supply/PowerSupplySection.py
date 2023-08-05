from camel_model.CamelModel import CamelModel

from sql_models.motorcycle_model.sections.power_supply.PowerSupplyComponent import PowerSupplyComponent


class PowerSupplySection(CamelModel):
    components: list[PowerSupplyComponent]
