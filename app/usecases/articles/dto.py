from app.usecases.shared.base_dto import BaseDto


class ArticleDto(BaseDto):
    description: str
    user_id: str
