from sqlmodel import select

from app.db.session import SessionDep
from app.exceptions.data_not_found_exception import DataNotFoundException
from app.exceptions.resource_ownership_exception import (
    ResourceOwnershipException,
)
from app.models.model import Article
from app.shared.study_pal_pydantic_base_model import StudyPalPydanticBaseModel


class DeleteCommand(StudyPalPydanticBaseModel):
    article_id: str
    user_id: str


class DeleteAction:
    def __init__(self, session: SessionDep) -> None:
        self._session = session

    def execute(self, command: DeleteCommand) -> None:
        article_model = self._session.exec(
            select(Article).where(Article.id == command.article_id)
        ).one_or_none()

        if article_model is None:
            raise DataNotFoundException("Article")

        if command.user_id != article_model.user_id:
            raise ResourceOwnershipException("Article")

        Article.delete(article_model, self._session)
        self._session.commit()
