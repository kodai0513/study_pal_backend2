from typing import cast

from sqlmodel import select

from app.db.session import SessionDep
from app.domain.services.selection_problem import (
    SelectionProblem as SelectionProblemProtcol,
)
from app.domain.services.selection_problem import (
    SelectionProblemService,
)
from app.exceptions.data_not_found_exception import DataNotFoundException
from app.exceptions.resource_ownership_exception import (
    ResourceOwnershipException,
)
from app.models.model import (
    DescriptionProblem,
    SelectionProblem,
    TrueOrFalseProblem,
    Workbook,
)
from app.schemas.resources.problem import CreateProblemReq
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
            SelectionProblemService.validate_multiple_choices(
                cast(SelectionProblemProtcol, v)
            )

            SelectionProblemService.validate_single_correct_answer(
                cast(SelectionProblemProtcol, v)
            )

            SelectionProblemService.validate_same_statement(
                cast(SelectionProblemProtcol, v)
            )

        workbook_id_field = {"workbook_id": command.workbook_id}
        new_description_problem_models = DescriptionProblem.bulk_insert(
            [
                v.model_dump() | workbook_id_field
                for v in command.description_problems
            ],
            self._session,
        )
        new_selection_problem_models = SelectionProblem.bulk_insert(
            [
                v.model_dump() | workbook_id_field
                for v in command.selection_problems
            ],
            self._session,
        )
        new_true_or_false_problem_models = TrueOrFalseProblem.bulk_insert(
            [
                v.model_dump() | workbook_id_field
                for v in command.true_or_false_problems
            ],
            self._session,
        )

        self._session.commit()

        return ProblemDto.model_validate(
            {
                "description_problems": new_description_problem_models,
                "selection_problems": new_selection_problem_models,
                "true_or_false_problems": new_true_or_false_problem_models,
            }
        )
