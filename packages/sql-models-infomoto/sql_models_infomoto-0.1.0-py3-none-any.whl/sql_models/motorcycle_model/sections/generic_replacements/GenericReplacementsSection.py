from camel_model.CamelModel import CamelModel

from sql_models.motorcycle_model.sections.generic_replacements.GenericReplacement import GenericReplacement


class GenericReplacementsSection(CamelModel):
    replacements: list[GenericReplacement]
