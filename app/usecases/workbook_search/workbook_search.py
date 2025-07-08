from sqlmodel import or_, select

from app.db.session import SessionDep
from app.models.model import Workbook
from app.schemas.contents.workbook import WorkbookListContent
from app.shared.study_pal_pydantic_base_model import StudyPalPydanticBaseModel
from app.usecases.workbook_search.dto import WorkbookSearchDto


class WorkbookSearchCommand(StudyPalPydanticBaseModel):
    keyword: str


class WorkbookSearchAction:
    def __init__(self, session: SessionDep) -> None:
        self._session = session

    def execute(self, command: WorkbookSearchCommand) -> WorkbookSearchDto:
        keyword_pattern = f"%{command.keyword}%"
        statement = select(
            Workbook.id, Workbook.description, Workbook.title
        ).where(
            or_(
                Workbook.title.like(keyword_pattern),  # type: ignore
                Workbook.description.like(keyword_pattern),  # type: ignore
            )
        )
        workbooks = self._session.exec(statement).all()

        article_contents = [
            WorkbookListContent(id=id, description=description, title=title)
            for id, description, title in workbooks
        ]

        return WorkbookSearchDto(data=article_contents)
