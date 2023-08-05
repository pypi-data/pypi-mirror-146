from sql_models.shared.text.VerticalMarkdown import VerticalMarkdown

from sql_models.motorcycle_model.sections.abs.AbsProblem import AbsProblem


class AbsSection(VerticalMarkdown):
    problems: list[AbsProblem]
