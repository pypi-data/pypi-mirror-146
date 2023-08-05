from camel_model.CamelModel import CamelModel

from sql_models.motorcycle_model.sections.tightening_specifications.TighteningSpecificationElementPart import \
    TighteningSpecificationElementPart


class TighteningSpecificationElement(CamelModel):
    name: str | None
    parts: list[TighteningSpecificationElementPart]
