from camel_model.CamelModel import CamelModel

from sql_models.motorcycle_model.sections.tightening_specifications.TighteningSpecificationElement import \
    TighteningSpecificationElement


class TighteningSpecificationsSection(CamelModel):
    tightening_specifications: list[TighteningSpecificationElement] | None
