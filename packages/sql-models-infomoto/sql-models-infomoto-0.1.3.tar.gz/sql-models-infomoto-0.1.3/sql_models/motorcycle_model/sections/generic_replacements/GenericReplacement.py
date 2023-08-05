from camel_model.CamelModel import CamelModel

from sql_models.motorcycle_model.sections.generic_replacements.GenericReplacementPart import GenericReplacementPart


class GenericReplacement(CamelModel):
    name: str | None
    reference: str | None
    observations: str | None
    parts: list[GenericReplacementPart]
