from app.schemas.contents.article import ArticleContent
from app.schemas.shared.page_info import PageInfo
from app.shared.study_pal_pydantic_base_model import StudyPalPydanticBaseModel


class TimelineViewResp(StudyPalPydanticBaseModel):
    data: list[ArticleContent]
    page_info: PageInfo
