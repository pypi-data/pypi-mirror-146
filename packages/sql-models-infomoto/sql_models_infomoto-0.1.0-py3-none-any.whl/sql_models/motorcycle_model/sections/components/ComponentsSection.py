from camel_model.CamelModel import CamelModel

from sql_models.motorcycle_model.sections.components.Component import Component
from sql_models.shared.image.ImageFile import ImageFile


class ComponentsSection(CamelModel):
    components: list[Component]
    components_image: ImageFile | None
