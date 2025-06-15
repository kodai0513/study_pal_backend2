from sqlmodel import select

from app.db.session import SessionDep
from app.exceptions.data_not_found_exception import DataNotFoundException
from app.models.model import DescriptionProblem
from app.schemas.description_problem import UpdateDescriptionProblemReq
from app.usecases.description_problems.dto import DescriptionProblemDto


class UpdateCommand(UpdateDescriptionProblemReq):
    description_problem_id: str
    workbook_id: str


class UpdateAction:
    def __init__(self, session: SessionDep) -> None:
        self._session = session

    def execute(self, command: UpdateCommand) -> DescriptionProblemDto:
        description_problem_model = self._session.exec(
            select(DescriptionProblem).where(
                DescriptionProblem.id == command.description_problem_id,
                DescriptionProblem.workbook_id == command.workbook_id,
            )
        ).one_or_none()

        if description_problem_model is None:
            raise DataNotFoundException("DescriptionProblem")

        update_values = command.model_dump(
            exclude_unset=True,
            exclude={"description_problem_id", "workbook_id"},
        )
        updated_description_problem_model = DescriptionProblem.update(
            command.description_problem_id, self._session, update_values
        )
        self._session.commit()

        return DescriptionProblemDto.model_validate(
            updated_description_problem_model
        )
