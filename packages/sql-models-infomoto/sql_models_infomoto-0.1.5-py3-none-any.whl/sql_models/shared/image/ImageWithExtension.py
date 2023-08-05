from sql_models.shared.image.Image import Image
from sql_models.shared.file.FileExtension import FileExtension


class ImageWithExtension(Image, FileExtension):
    pass
