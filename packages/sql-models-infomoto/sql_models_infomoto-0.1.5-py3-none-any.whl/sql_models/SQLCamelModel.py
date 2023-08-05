from camel_model.CamelModel import CamelModel
from sqlmodel import SQLModel


class SQLCamelModel(CamelModel, SQLModel):
    pass
