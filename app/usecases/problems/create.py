from sqlmodel import select

from app.db.session import SessionDep
from app.domain.services.selection_problem_answer import (
    SelectionProblemAnswerService,
)
from app.exceptions.data_not_found_exception import DataNotFoundException
from app.exceptions.resource_ownership_exception import (
    ResourceOwnershipException,
)
from app.exceptions.selection_problem_answers.invalid_single_correct_answer_exception import (  # noqa
    InvalidSingleCorrectAnswerException,
)
from app.models.model import (
    DescriptionProblem,
    SelectionProblem,
    SelectionProblemAnswer,
    TrueOrFalseProblem,
    Workbook,
)
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

        for v in command.selection_problems:
            if not SelectionProblemAnswerService.has_only_one_correct_answer(
                v.selection_problem_answers
            ):
                raise InvalidSingleCorrectAnswerException

        new_article_model = DescriptionProblem.bulk_insert(
            [v.model_dump() for v in command.description_problems],
            self._session,
        )
        self._session.commit()

        return ProblemDto.model_validate(new_article_model)
