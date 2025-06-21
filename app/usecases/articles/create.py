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
        new_article_model = Article.insert(command.model_dump(), self._session)
        self._session.commit()
        return ArticleDto.model_validate(new_article_model)
