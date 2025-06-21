from sqlmodel import select

from app.db.session import SessionDep
from app.exceptions.data_not_found_exception import DataNotFoundException
from app.models.model import TrueOrFalseProblem
from app.shared.study_pal_pydantic_base_model import StudyPalPydanticBaseModel


class DeleteCommand(StudyPalPydanticBaseModel):
    true_or_false_problem_id: str
    workbook_id: str


class DeleteAction:
    def __init__(self, session: SessionDep) -> None:
        self._session = session

    def execute(self, command: DeleteCommand) -> None:
        true_or_false_problem_model = self._session.exec(
            select(TrueOrFalseProblem).where(
                TrueOrFalseProblem.id == command.true_or_false_problem_id,
                TrueOrFalseProblem.workbook_id == command.workbook_id,
            )
        ).one_or_none()

        if true_or_false_problem_model is None:
            raise DataNotFoundException("TrueOrFalseProblem")

        TrueOrFalseProblem.delete(true_or_false_problem_model, self._session)

        self._session.commit()
