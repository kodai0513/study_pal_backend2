from typing import Sequence

from sqlalchemy.orm import load_only
from sqlmodel import desc, select

from app.db.session import SessionDep
from app.middlewares.auth import AuthDep
from app.models.model import Workbook
from app.schemas.contents.workbook import WorkbookListContent
from app.schemas.shared.page_info import PageInfo
from app.shared.study_pal_pydantic_base_model import StudyPalPydanticBaseModel
from app.usecases.shared.pagination import pagination
from app.usecases.workbook_me.dto import WorkbookMeDto


class WorkbookMeCommand(StudyPalPydanticBaseModel):
    authUser: AuthDep
    page_info: PageInfo


class WorkbookMeAction:
    def __init__(self, session: SessionDep) -> None:
        self._session = session

    def execute(self, command: WorkbookMeCommand) -> WorkbookMeDto:
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
            .where(Workbook.user_id == command.authUser.user_id)
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

        return WorkbookMeDto(data=article_contents, page_info=page_info)
