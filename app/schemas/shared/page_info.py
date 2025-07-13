from app.shared.study_pal_pydantic_base_model import StudyPalPydanticBaseModel


class PageInfo(StudyPalPydanticBaseModel):
    next_page_token: str | None
    page_size: int
