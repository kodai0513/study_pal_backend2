from pydantic import Field

from app.schemas.shared.id_response_schema import IdResponseSchema
from app.schemas.shared.time_response_schema import TimeResponseSchema
from app.shared.study_pal_pydantic_base_model import StudyPalPydanticBaseModel


class CreateSelectionProblemAnswerReq(StudyPalPydanticBaseModel):
    is_correct: bool
    statement: str = Field(max_length=255)


class UpdateSelectionProblemAnswerReq(StudyPalPydanticBaseModel):
    is_correct: bool
    statement: str = Field(max_length=255)


class SelectionProblemAnswerResp(IdResponseSchema, TimeResponseSchema):
    is_correct: bool
    selection_problem_id: str
    statement: str = Field(max_length=255)
