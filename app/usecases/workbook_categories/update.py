from sqlmodel import select

from app.db.session import SessionDep
from app.exceptions.data_not_found_exception import DataNotFoundException
from app.models.model import Workbook
from app.schemas.workbook import UpdateWorkbookReq
from app.usecases.workbooks.dto import WorkbookDto


class UpdateCommand(UpdateWorkbookReq):
    user_id: str
    workbook_id: str


class UpdateAction:
    def __init__(self, session: SessionDep) -> None:
        self._session = session

    def execute(self, command: UpdateCommand) -> WorkbookDto:
        workbook_model = self._session.exec(
            select(Workbook).where(Workbook.id == command.workbook_id)
        ).one_or_none()

        if workbook_model is None:
            raise DataNotFoundException("Workbook")

        update_values = command.model_dump(
            exclude_unset=True, exclude={"workbook_id", "user_id"}
        )
        updated_workbook_model = Workbook.update_by_id(
            command.workbook_id, self._session, update_values
        )
        self._session.commit()

        return WorkbookDto.model_validate(updated_workbook_model)
