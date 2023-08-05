from typing import Optional

from sql_models.shared.text.TextLine import TextLine
from sql_models.shared.text.VerticalMarkdown import VerticalMarkdown

from sql_models.motorcycle_model.sections.hiss_immobilizer.HissImmobilizerProblem import HissImmobilizerProblem


class HissImmobilizerSection(VerticalMarkdown):
    key_cloning_steps: list[TextLine]
    errors: list[TextLine]
    problems: list[HissImmobilizerProblem]
    key_coding_problems: list[HissImmobilizerProblem]
