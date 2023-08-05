from camel_model.CamelModel import CamelModel

from sql_models.motorcycle_model.sections.tightening_specifications.TighteningSpecificationScrewStep import \
    TighteningSpecificationScrewStep


class TighteningSpecificationPartScrew(CamelModel):
    name: str | None
    tightening_specification: str | None
    steps: list[TighteningSpecificationScrewStep] | None
    detail: str | None
