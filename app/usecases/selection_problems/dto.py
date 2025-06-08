from app.usecases.shared.id_dto import IdDto
from app.usecases.shared.time_dto import TimeDto


class SelectionProblemAnswer(IdDto, TimeDto):
    is_correct: bool
    selection_problem_id: str
    statement: str


class SelectionProblemDto(IdDto, TimeDto):
    answers: list[SelectionProblemAnswer]
    statement: str
    workbook_id: str
    workbook_category_id: str | None
