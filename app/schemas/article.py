from pydantic import Field

from app.schemas.shared.id_response_schema import IdResponseSchema
from app.schemas.shared.time_response_schema import TimeResponseSchema
from app.shared.study_pal_pydantic_base_model import StudyPalPydanticBaseModel


class CreateArticleReq(StudyPalPydanticBaseModel):
    description: str = Field(max_length=400)


class UpdateArticleReq(StudyPalPydanticBaseModel):
    description: str = Field(max_length=400)


class ArticleResp(IdResponseSchema, TimeResponseSchema):
    description: str
    page_id: int | None
    user_id: str
