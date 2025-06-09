from pydantic import Field

from app.schemas.selection_problem_answer import (
    CreateSelectionProblemAnswerReq,
    SelectionProblemAnswerResp,
    UpdateSelectionProblemAnswerReq,
)
from app.schemas.shared.id_response_schema import IdResponseSchema
from app.schemas.shared.time_response_schema import TimeResponseSchema
from app.shared.study_pal_pydantic_base_model import StudyPalPydanticBaseModel


class CreateSelectionProblemReq(StudyPalPydanticBaseModel):
    answers: list[CreateSelectionProblemAnswerReq]
    statement: str = Field(max_length=255)
    workbook_category_id: str | None


class UpdateSelectionProblemReq(StudyPalPydanticBaseModel):
    answers: UpdateSelectionProblemAnswerReq
    statement: str = Field(max_length=255)
    workbook_category_id: str | None


class SelectionProblemResp(IdResponseSchema, TimeResponseSchema):
    answers: SelectionProblemAnswerResp
    statement: str = Field(max_length=255)
    workbook_id: str
    workbook_category_id: str | None
