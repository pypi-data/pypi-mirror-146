from camel_model.CamelModel import CamelModel

from sql_models.motorcycle_model.sections.engine.EngineElementAttribute import EngineElementAttribute


class EngineSubsectionElement(CamelModel):
    name: str | None
    value: str | None
    observations: str | None
    attributes: list[EngineElementAttribute] | None
