from camel_model.CamelModel import CamelModel

from sql_models.shared.image.ImageFile import ImageFile
from sql_models.shared.text.TextLine import TextLine


class DataBlock(CamelModel):
    text_lines: list[TextLine] | None
    image: ImageFile | None
    upper_text: bool | None