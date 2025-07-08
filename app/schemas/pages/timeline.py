from app.schemas.shared.page_info import PageInfo
from app.schemas.views.article import ArticleView
from app.shared.study_pal_pydantic_base_model import StudyPalPydanticBaseModel


class TimelineResp(StudyPalPydanticBaseModel):
    data: list[ArticleView]
    page_info: PageInfo
