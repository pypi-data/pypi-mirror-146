from camel_model.CamelModel import CamelModel


class AbsProblem(CamelModel):
    code: str | None
    involved_element: str | None
    description: str | None
