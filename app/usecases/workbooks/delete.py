from sqlmodel import select

from app.db.session import SessionDep
from app.exceptions.data_not_found_exception import DataNotFoundException
from app.models.model import Workbook
from app.shared.study_pal_pydantic_base_model import StudyPalPydanticBaseModel


class DeleteCommand(StudyPalPydanticBaseModel):
    user_id: str
    workbook_id: str


class DeleteAction:
    def __init__(self, session: SessionDep) -> None:
        self._session = session

    def execute(self, command: DeleteCommand) -> None:
        workbook_model = self._session.exec(
            select(Workbook).where(Workbook.id == command.workbook_id)
        ).one_or_none()

        if workbook_model is None:
            raise DataNotFoundException("Workbook")

        Workbook.delete(workbook_model, self._session)
        self._session.commit()
