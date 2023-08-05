from camel_model.CamelModel import CamelModel

from sql_models.motorcycle_model.sections.tightening_specifications.TighteningSpecificationPartScrew import \
    TighteningSpecificationPartScrew


class TighteningSpecificationElementPart(CamelModel):
    name: str | None
    screws: list[TighteningSpecificationPartScrew] | None
