from app.shared.study_pal_pydantic_base_model import StudyPalPydanticBaseModel


class IdDto(StudyPalPydanticBaseModel):
    id: str
