from app.schemas.shared.id_response_schema import IdResponseSchema


class ArticleContent(IdResponseSchema):
    description: str
    user_id: str
    user_name: str
    user_nickname: str | None
