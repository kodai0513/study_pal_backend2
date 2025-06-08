from app.usecases.shared.id_dto import IdDto
from app.usecases.shared.time_dto import TimeDto


class TrueOrFalseProblemDto(IdDto, TimeDto):
    is_correct: bool
    statement: str
    workbook_id: str
    workbook_category_id: str | None
