from camel_model.CamelModel import CamelModel


class SmartKeyFault(CamelModel):
    fault_kind: list[TextLine]
    flash_pattern_image: NewImageData | None
    flashs_number_by_time: str | None
    parts_to_review: list[TextLine] | None