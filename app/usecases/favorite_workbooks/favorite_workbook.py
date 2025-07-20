from typing import Sequence

from sqlalchemy.orm import selectinload, with_loader_criteria
from sqlmodel import desc, select

from app.db.session import SessionDep
from app.middlewares.auth import AuthDep
from app.models.model import FavoriteWorkbook, Workbook
from app.schemas.contents.workbook import WorkbookListContent
from app.schemas.shared.page_info import PageInfo
from app.shared.study_pal_pydantic_base_model import StudyPalPydanticBaseModel
from app.usecases.favorite_workbooks.dto import FavoriteWorkbookDto
from app.usecases.shared.pagination import pagination


class FavoriteWorkbookCommand(StudyPalPydanticBaseModel):
    authUser: AuthDep
    page_info: PageInfo


class FavoriteWorkbookAction:
    def __init__(self, session: SessionDep) -> None:
        self._session = session

    def execute(self, command: FavoriteWorkbookCommand) -> FavoriteWorkbookDto:
        limit = command.page_info.page_size + 1
        base_statement = (
            select(FavoriteWorkbook)
            .options(
                selectinload(FavoriteWorkbook.workbook).load_only(
                    Workbook.id,
                    Workbook.title,
                    Workbook.description,
                ),
                with_loader_criteria(
                    Workbook, Workbook.is_public, include_aliases=True
                ),
            )
            .where(FavoriteWorkbook.user_id == command.authUser.user_id)
        )

        def base_query() -> Sequence[Workbook]:
            result = self._session.exec(
                base_statement.order_by(desc(FavoriteWorkbook.id)).limit(limit)
            ).all()

            return [v.workbook for v in result if v.workbook is not None]

        def next_query() -> Sequence[Workbook]:
            if command.page_info.next_page_token is None:
                raise ValueError("next_page_token is required but was None.")
            result = self._session.exec(
                base_statement.where(
                    FavoriteWorkbook.id <= command.page_info.next_page_token
                )
                .order_by(desc(FavoriteWorkbook.id))
                .limit(limit)
            ).all()

            return [v.workbook for v in result if v.workbook is not None]

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

        return FavoriteWorkbookDto(data=article_contents, page_info=page_info)
