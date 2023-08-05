from typing import Optional

from camel_model.CamelModel import CamelModel


class AutodiagnosisFault(CamelModel):
    code: Optional[str]
    description: Optional[str]
    observations: Optional[str]
