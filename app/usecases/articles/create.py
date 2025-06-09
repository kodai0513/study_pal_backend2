from app.db.session import SessionDep
from app.models.model import Article
from app.schemas.article import CreateArticleReq
from app.usecases.articles.dto import ArticleDto


class CreateCommand(CreateArticleReq):
    user_id: str


class CreateAction:
    def __init__(self, session: SessionDep) -> None:
        self._session = session

    def execute(self, command: CreateCommand) -> ArticleDto:
        article_model = Article.model_validate(command)

        new_article_model = Article.update_or_insert(
            article_model, self._session
        )
        self._session.commit()

        return ArticleDto.model_validate(new_article_model)
