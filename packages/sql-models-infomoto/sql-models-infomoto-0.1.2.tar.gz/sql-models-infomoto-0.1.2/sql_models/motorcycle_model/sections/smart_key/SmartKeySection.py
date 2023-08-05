from sql_models.shared.text.VerticalMarkdown import VerticalMarkdown

from sql_models.motorcycle_model.sections.smart_key.SmartKeyFault import SmartKeyFault


class SmartKeySection(VerticalMarkdown):
    faults: list[SmartKeyFault]
