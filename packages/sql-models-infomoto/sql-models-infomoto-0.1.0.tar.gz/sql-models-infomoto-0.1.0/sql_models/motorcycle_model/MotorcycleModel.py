from camel_model.CamelModel import CamelModel

from sql_models.shared.image.ImageWithExtension import ImageWithExtension

from sql_models.motorcycle_model.sections.MotorcycleModelSections import MotorcycleModelSections


class MotorcycleModel(CamelModel):
    model_name: str
    model_image: ImageWithExtension | None
    sections: MotorcycleModelSections
