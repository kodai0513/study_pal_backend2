from app.schemas.contents.workbook import WorkbookListContent
from app.schemas.shared.page_info import PageInfo
from app.shared.study_pal_pydantic_base_model import StudyPalPydanticBaseModel


class WorkbookListsViewResp(StudyPalPydanticBaseModel):
    data: list[WorkbookListContent]
    page_info: PageInfo
