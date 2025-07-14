from typing import Sequence

from sqlalchemy.orm import load_only
from sqlmodel import desc, or_, select

from app.db.session import SessionDep
from app.models.model import Workbook
from app.schemas.contents.workbook import WorkbookListContent
from app.schemas.shared.page_info import PageInfo
from app.shared.study_pal_pydantic_base_model import StudyPalPydanticBaseModel
from app.usecases.shared.pagination import pagination
from app.usecases.workbook_search.dto import WorkbookSearchDto


class WorkbookSearchCommand(StudyPalPydanticBaseModel):
    keyword: str
    page_info: PageInfo


class WorkbookSearchAction:
    def __init__(self, session: SessionDep) -> None:
        self._session = session

    def execute(self, command: WorkbookSearchCommand) -> WorkbookSearchDto:
        keyword_pattern = f"%{command.keyword}%"
        limit = command.page_info.page_size + 1
        base_statement = (
            select(Workbook)
            .options(
                load_only(
                    Workbook.id,  # type: ignore
                    Workbook.title,  # type: ignore
                    Workbook.description,  # type: ignore
                )
            )
            .where(
                or_(
                    Workbook.title.like(keyword_pattern),  # type: ignore
                    Workbook.description.like(keyword_pattern),  # type: ignore
                ),
                Workbook.is_public is True,
            )
        )

        def base_query() -> Sequence[Workbook]:
            return self._session.exec(
                base_statement.order_by(desc(Workbook.id)).limit(limit)
            ).all()

        def next_query() -> Sequence[Workbook]:
            if command.page_info.next_page_token is None:
                raise ValueError("next_page_token is required but was None.")
            return self._session.exec(
                base_statement.where(
                    Workbook.id <= command.page_info.next_page_token
                )
                .order_by(desc(Workbook.id))
                .limit(limit)
            ).all()

        workbooks, page_info = pagination(
            base_query=base_query,
            next_query=next_query,
            page=command.page_info,
        )

        article_contents = [
            WorkbookListContent(
                id=v.id, description=v.description, title=v.title
            )
            for v in workbooks
        ]

        return WorkbookSearchDto(data=article_contents, page_info=page_info)
