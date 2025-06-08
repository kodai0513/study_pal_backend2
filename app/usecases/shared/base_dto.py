import datetime

from app.shared.study_pal_pydantic_base_model import StudyPalPydanticBaseModel


class BaseDto(StudyPalPydanticBaseModel):
    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
