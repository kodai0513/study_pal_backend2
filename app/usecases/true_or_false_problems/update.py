from sqlmodel import select

from app.db.session import SessionDep
from app.exceptions.data_not_found_exception import DataNotFoundException
from app.models.model import TrueOrFalseProblem
from app.schemas.true_or_false_problem import UpdateTrueOrFalseProblemReq
from app.usecases.true_or_false_problems.dto import TrueOrFalseProblemDto


class UpdateCommand(UpdateTrueOrFalseProblemReq):
    true_or_false_problem_id: str
    workbook_id: str


class UpdateAction:
    def __init__(self, session: SessionDep) -> None:
        self._session = session

    def execute(self, command: UpdateCommand) -> TrueOrFalseProblemDto:
        true_or_false_problem_model = self._session.exec(
            select(TrueOrFalseProblem).where(
                TrueOrFalseProblem.id == command.true_or_false_problem_id,
                TrueOrFalseProblem.workbook_id == command.workbook_id,
            )
        ).one_or_none()

        if true_or_false_problem_model is None:
            raise DataNotFoundException("TrueOrFalseProblem")

        update_values = command.model_dump(
            exclude_unset=True,
            exclude={"true_or_false_problem_id", "workbook_id"},
        )
        updated_true_or_false_problem_model = TrueOrFalseProblem.update_by_id(
            command.true_or_false_problem_id, self._session, update_values
        )
        self._session.commit()

        return TrueOrFalseProblemDto.model_validate(
            updated_true_or_false_problem_model
        )
