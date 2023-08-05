from camel_model.CamelModel import CamelModel

from sql_models.motorcycle_model.sections.components.ComponentsSection import ComponentsSection
from sql_models.motorcycle_model.sections.distribution.DistributionSection import DistributionSection
from sql_models.motorcycle_model.sections.engine.EngineSection import EngineSection
from sql_models.motorcycle_model.sections.power_supply.PowerSupplySection import PowerSupplySection
from sql_models.shared.page.PagesImages import PagesImages

from sql_models.motorcycle_model.sections.generic_replacements.GenericReplacementsSection import \
    GenericReplacementsSection
from sql_models.motorcycle_model.sections.autodiagnosis.AutodiagnosisSection import AutodiagnosisSection
from sql_models.motorcycle_model.sections.abs.AbsSection import AbsSection
from sql_models.motorcycle_model.sections.custom_electrical_scheme.CustomElectricalScheme import CustomElectricalScheme
from sql_models.motorcycle_model.sections.frame.FrameSection import FrameSection
from sql_models.motorcycle_model.sections.hiss_immobilizer.HissImmobilizerSection import HissImmobilizerSection
from sql_models.motorcycle_model.sections.smart_key.SmartKeySection import SmartKeySection


class MotorcycleModelSections(CamelModel):
    generic_replacements: GenericReplacementsSection | None

    engine: EngineSection | None
    frame: FrameSection | None
    power_supply: PowerSupplySection | None
    distribution: DistributionSection | None
    components_data: ComponentsSection | None
    autodiagnosis: AutodiagnosisSection | None
    abs: AbsSection | None
    smart_key: SmartKeySection | None
    frame: FrameSection | None
    hiss_immobilizer: HissImmobilizerSection | None

    user_manual: PagesImages | None
    workshop_manual: PagesImages | None
    reduced_data_sheet: PagesImages | None
    components_location: PagesImages | None
    electrical_scheme: PagesImages | None

    custom_electrical_scheme_1: CustomElectricalScheme | None
    custom_electrical_scheme_2: CustomElectricalScheme | None
