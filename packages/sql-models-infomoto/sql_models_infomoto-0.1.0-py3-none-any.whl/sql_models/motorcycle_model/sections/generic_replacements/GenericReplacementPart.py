from camel_model.CamelModel import CamelModel


class GenericReplacementPart(CamelModel):
    name: str | None
    reference: str | None
    observations: str | None
