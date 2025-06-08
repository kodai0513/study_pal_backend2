from pydantic import Field

from app.schemas.shared.id_response_schema import IdResponseSchema
from app.schemas.shared.time_response_schema import TimeResponseSchema
from app.shared.study_pal_pydantic_base_model import StudyPalPydanticBaseModel


class CreateTrueOrFalseProblemReq(StudyPalPydanticBaseModel):
    is_correct: bool
    statement: str = Field(max_length=255)
    workbook_category_id: str | None


class UpdateTrueOrFalseProblemReq(StudyPalPydanticBaseModel):
    is_correct: bool
    statement: str = Field(max_length=255)
    workbook_category_id: str | None


class TrueOrFalseProblemResp(IdResponseSchema, TimeResponseSchema):
    is_correct: bool
    statement: str = Field(max_length=255)
    workbook_id: str
    workbook_category_id: str | None
