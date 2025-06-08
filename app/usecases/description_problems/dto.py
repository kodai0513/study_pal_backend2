from app.usecases.shared.id_dto import IdDto
from app.usecases.shared.time_dto import TimeDto


class DescriptionProblemDto(IdDto, TimeDto):
    correct_statement: str
    statement: str
    workbook_id: str
    workbook_category_id: str | None
