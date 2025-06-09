from sqlmodel import select

from app.db.session import SessionDep
from app.exceptions.data_not_found_exception import DataNotFoundException
from app.exceptions.resource_ownership_exception import (
    ResourceOwnershipException,
)
from app.models.model import Article, Workbook
from app.schemas.problem import CreateProblemReq
from app.usecases.problems.dto import ProblemDto


class CreateCommand(CreateProblemReq):
    user_id: str
    workbook_id: str


class CreateAction:
    def __init__(self, session: SessionDep) -> None:
        self._session = session

    def execute(self, command: CreateCommand) -> ProblemDto:
        workbook_model = self._session.exec(
            select(Workbook).where(Workbook.id == command.workbook_id)
        ).one_or_none()

        if workbook_model is None:
            raise DataNotFoundException("Workbook")

        if command.user_id != workbook_model.user_id:
            raise ResourceOwnershipException("Problem")

        article_model = Article.model_validate(command)

        new_article_model = Article.update_or_insert(
            article_model, self._session
        )
        self._session.commit()

        return ProblemDto.model_validate(new_article_model)
