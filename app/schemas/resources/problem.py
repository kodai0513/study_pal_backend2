from app.schemas.resources.description_problem import (
    CreateDescriptionProblemReq,
    DescriptionProblemResp,
)
from app.schemas.resources.selection_problem import (
    CreateSelectionProblemReq,
    SelectionProblemResp,
)
from app.schemas.resources.true_or_false_problem import (
    CreateTrueOrFalseProblemReq,
    TrueOrFalseProblemResp,
)
from app.shared.study_pal_pydantic_base_model import StudyPalPydanticBaseModel


class CreateProblemReq(StudyPalPydanticBaseModel):
    description_problems: list[CreateDescriptionProblemReq]
    selection_problems: list[CreateSelectionProblemReq]
    true_or_false_problems: list[CreateTrueOrFalseProblemReq]


class ProblemResp(StudyPalPydanticBaseModel):
    description_problems: list[DescriptionProblemResp]
    selection_problems: list[SelectionProblemResp]
    true_or_false_problems: list[TrueOrFalseProblemResp]
