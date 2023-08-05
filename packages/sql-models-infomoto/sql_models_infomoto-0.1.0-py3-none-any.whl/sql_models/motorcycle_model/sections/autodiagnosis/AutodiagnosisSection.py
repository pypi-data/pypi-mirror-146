from sql_models.shared.text.VerticalMarkdown import VerticalMarkdown

from sql_models.motorcycle_model.sections.autodiagnosis.AutodiagnosisFault import AutodiagnosisFault


class AutodiagnosisSection(VerticalMarkdown):
    faults: list[AutodiagnosisFault]
