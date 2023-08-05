from camel_model.CamelModel import CamelModel

from sql_models.shared.page.PageImage import PageImage


class PagesImages(CamelModel):
    pages: list[PageImage] | None
