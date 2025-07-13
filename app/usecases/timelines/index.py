from typing import Sequence

from sqlalchemy.orm import selectinload
from sqlmodel import desc, select

from app.db.session import SessionDep
from app.models.model import Article
from app.schemas.contents.article import ArticleContent
from app.schemas.shared.page_info import PageInfo
from app.shared.study_pal_pydantic_base_model import StudyPalPydanticBaseModel
from app.usecases.shared.pagination import pagination
from app.usecases.timelines.dto import TimelineDto


class IndexCommand(StudyPalPydanticBaseModel):
    page_info: PageInfo


class IndexAction:
    def __init__(self, session: SessionDep) -> None:
        self._session = session

    def execute(self, command: IndexCommand) -> TimelineDto:
        limit = command.page_info.page_size + 1

        def base_query() -> Sequence[Article]:
            return self._session.exec(
                select(Article)
                .options(selectinload(Article.user))  # type: ignore
                .order_by(desc(Article.id))
                .limit(limit)
            ).all()

        def next_query() -> Sequence[Article]:
            if command.page_info.next_page_token is None:
                raise ValueError("next_page_token is required but was None.")
            return self._session.exec(
                select(Article)
                .options(selectinload(Article.user))  # type: ignore
                .where(Article.id <= command.page_info.next_page_token)
                .order_by(desc(Article.id))
                .limit(limit)
            ).all()

        articles, page_info = pagination(
            base_query, next_query, command.page_info
        )

        article_contents = [
            ArticleContent(
                id=v.id,
                description=v.description,
                user_id=v.user.id,
                user_name=v.user.name,
                user_nickname=v.user.nick_name,
            )
            for v in articles
        ]

        return TimelineDto(data=article_contents, page_info=page_info)
