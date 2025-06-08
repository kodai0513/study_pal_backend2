from pydantic import Field

from app.schemas.base_rest_response_schema import BaseRestResponseSchema
from app.shared.study_pal_pydantic_base_model import StudyPalPydanticBaseModel


class CreateArticleReq(StudyPalPydanticBaseModel):
    description: str = Field(max_length=400)


class CreateArticleResp(BaseRestResponseSchema):
    description: str
    user_id: str


class UpdateArticleReq(StudyPalPydanticBaseModel):
    description: str = Field(max_length=400)


class UpdateArticleResp(BaseRestResponseSchema):
    description: str
    user_id: str
