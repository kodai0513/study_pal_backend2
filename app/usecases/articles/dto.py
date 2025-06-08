from app.usecases.shared.id_dto import IdDto
from app.usecases.shared.time_dto import TimeDto


class ArticleDto(IdDto, TimeDto):
    page_id: int | None
    description: str
    user_id: str
