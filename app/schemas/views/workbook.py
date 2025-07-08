from app.schemas.contents.workbook import WorkbookListContent
from app.shared.study_pal_pydantic_base_model import StudyPalPydanticBaseModel


class WorkbookListsViewResp(StudyPalPydanticBaseModel):
    data: list[WorkbookListContent]
