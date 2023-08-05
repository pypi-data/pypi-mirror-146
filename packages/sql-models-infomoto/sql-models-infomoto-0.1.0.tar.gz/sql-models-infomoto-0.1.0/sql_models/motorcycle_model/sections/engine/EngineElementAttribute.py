from camel_model.CamelModel import CamelModel


class EngineElementAttribute(CamelModel):
    name: str | None
    value: str | None
    observations: str | None
