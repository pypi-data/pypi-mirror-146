from camel_model.CamelModel import CamelModel


class NewManufacturer(CamelModel):
    name: str

    def __init__(
            self,
            **data,
    ):
        super().__init__(**data)