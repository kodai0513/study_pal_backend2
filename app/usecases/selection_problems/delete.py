from sqlmodel import select

from app.db.session import SessionDep
from app.exceptions.data_not_found_exception import DataNotFoundException
from app.models.model import SelectionProblem
from app.shared.study_pal_pydantic_base_model import StudyPalPydanticBaseModel


class DeleteCommand(StudyPalPydanticBaseModel):
    selection_problem_id: str
    workbook_id: str


class DeleteAction:
    def __init__(self, session: SessionDep) -> None:
        self._session = session

    def execute(self, command: DeleteCommand) -> None:
        selection_problem = self._session.exec(
            select(SelectionProblem).where(
                SelectionProblem.id == command.selection_problem_id,
                SelectionProblem.workbook_id == command.workbook_id,
            )
        ).one_or_none()

        if selection_problem is None:
            raise DataNotFoundException("SelectionProblem")

        SelectionProblem.delete(selection_problem, self._session)

        self._session.commit()
