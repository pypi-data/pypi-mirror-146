from sql_models.motorcycle_model.sections.frame.FrameElementPart import FrameElementPart
from sql_models.shared.image.ImageFile import ImageFile


class FrameElement:
    name: str | None
    value: str | None
    observations: str | list[str] | None
    parts: list[FrameElementPart] | None
    image: ImageFile | None
