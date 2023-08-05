from camel_model.CamelModel import CamelModel

from sql_models.motorcycle_model.sections.engine.EngineSubsectionElement import EngineSubsectionElement


class EngineSubsection(CamelModel):
    name: str | None
    elements: list[EngineSubsectionElement] | None
