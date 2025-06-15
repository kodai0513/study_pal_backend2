from sqlmodel import select

from app.db.session import SessionDep
from app.exceptions.data_not_found_exception import DataNotFoundException
from app.models.model import DescriptionProblem
from app.shared.study_pal_pydantic_base_model import StudyPalPydanticBaseModel


class DeleteCommand(StudyPalPydanticBaseModel):
    description_problem_id: str
    workbook_id: str


class DeleteAction:
    def __init__(self, session: SessionDep) -> None:
        self._session = session

    def execute(self, command: DeleteCommand) -> None:
        description_problem_model = self._session.exec(
            select(DescriptionProblem).where(
                DescriptionProblem.id == command.description_problem_id,
                DescriptionProblem.workbook_id == command.workbook_id,
            )
        ).one_or_none()

        if description_problem_model is None:
            raise DataNotFoundException("DescriptionProblem")

        DescriptionProblem.delete(description_problem_model, self._session)

        self._session.commit()
