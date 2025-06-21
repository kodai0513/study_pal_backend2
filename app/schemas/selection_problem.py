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
    selection_problem_answers: list[CreateSelectionProblemAnswerReq]
    statement: str = Field(max_length=255)
    workbook_category_id: str | None


class UpdateSelectionProblemReq(StudyPalPydanticBaseModel):
    selection_problem_answers: list[UpdateSelectionProblemAnswerReq]
    statement: str = Field(max_length=255)
    workbook_category_id: str | None


class SelectionProblemResp(IdResponseSchema, TimeResponseSchema):
    selection_problem_answers: list[SelectionProblemAnswerResp]
    statement: str = Field(max_length=255)
    workbook_id: str
    workbook_category_id: str | None
