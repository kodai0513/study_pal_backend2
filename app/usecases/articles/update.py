from sqlmodel import select

from app.db.session import SessionDep
from app.exceptions.data_not_found_exception import DataNotFoundException
from app.exceptions.resource_ownership_exception import (
    ResourceOwnershipException,
)
from app.models.model import Article
from app.shared.study_pal_pydantic_base_model import StudyPalPydanticBaseModel
from app.usecases.articles.dto import ArticleDto


class UpdateCommand(StudyPalPydanticBaseModel):
    article_id: str
    description: str
    user_id: str


class UpdateAction:
    def __init__(self, session: SessionDep) -> None:
        self._session = session

    def execute(self, command: UpdateCommand) -> ArticleDto:
        article_model = self._session.exec(
            select(Article).where(Article.id == command.article_id)
        ).one_or_none()

        if article_model is None:
            raise DataNotFoundException("Article")

        if command.user_id != article_model.user_id:
            raise ResourceOwnershipException("Article")

        update_values = command.model_dump(
            exclude_unset=True, exclude={"article_id", "user_id"}
        )
        new_article_model = Article.update_or_insert(
            article_model, self._session, update_values
        )
        self._session.commit()

        return ArticleDto.model_validate(new_article_model)
