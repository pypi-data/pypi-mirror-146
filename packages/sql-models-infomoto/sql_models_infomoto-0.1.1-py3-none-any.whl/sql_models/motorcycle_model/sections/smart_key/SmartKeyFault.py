from camel_model.CamelModel import CamelModel

from sql_models.shared.image.ImageFile import ImageFile
from sql_models.shared.text.TextLine import TextLine


class SmartKeyFault(CamelModel):
    fault_kind: list[TextLine]
    flash_pattern_image: ImageFile | None
    flashs_number_by_time: str | None
    parts_to_review: list[TextLine] | None
