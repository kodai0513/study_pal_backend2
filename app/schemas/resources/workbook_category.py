from pydantic import Field

from app.schemas.shared.id_response_schema import IdResponseSchema
from app.schemas.shared.time_response_schema import TimeResponseSchema
from app.shared.study_pal_pydantic_base_model import StudyPalPydanticBaseModel


class CreateWorkbookCategoryReq(StudyPalPydanticBaseModel):
    title: str = Field(max_length=50)
    description: str = Field(max_length=400)


class UpdateWorkbookCategoryReq(StudyPalPydanticBaseModel):
    title: str = Field(max_length=50)
    description: str = Field(max_length=400)


class WorkbookCategoryResp(IdResponseSchema, TimeResponseSchema):
    description: str
    is_public: bool
    title: str
    user_id: str
