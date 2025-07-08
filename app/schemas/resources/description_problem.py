from pydantic import Field

from app.schemas.shared.id_response_schema import IdResponseSchema
from app.schemas.shared.time_response_schema import TimeResponseSchema
from app.shared.study_pal_pydantic_base_model import StudyPalPydanticBaseModel


class CreateDescriptionProblemReq(StudyPalPydanticBaseModel):
    correct_statement: str = Field(max_length=255)
    statement: str = Field(max_length=1000)
    workbook_category_id: str | None


class UpdateDescriptionProblemReq(StudyPalPydanticBaseModel):
    correct_statement: str = Field(max_length=255)
    statement: str = Field(max_length=1000)
    workbook_category_id: str | None


class DescriptionProblemResp(IdResponseSchema, TimeResponseSchema):
    correct_statement: str = Field(max_length=255)
    statement: str = Field(max_length=1000)
    workbook_id: str
    workbook_category_id: str | None
