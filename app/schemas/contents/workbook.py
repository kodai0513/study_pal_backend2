from app.schemas.shared.id_response_schema import IdResponseSchema


class WorkbookListContent(IdResponseSchema):
    description: str
    title: str


class WorkbookDetailContent(IdResponseSchema):
    description: str
    title: str
    user_name: str
    user_nickname: str | None
