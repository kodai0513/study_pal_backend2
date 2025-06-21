from app.constants.role import RoleId
from app.db.session import SessionDep
from app.models.model import Workbook, WorkbookMember
from app.schemas.workbook import CreateWorkbookReq
from app.usecases.workbooks.dto import WorkbookDto


class CreateCommand(CreateWorkbookReq):
    user_id: str


class CreateAction:
    def __init__(self, session: SessionDep) -> None:
        self._session = session

    def execute(self, command: CreateCommand) -> WorkbookDto:
        new_workbook_model = Workbook.insert(
            command.model_dump(), self._session
        )

        # 問題集作成時は作成者をオーナー権限で追加する
        self._session.add(
            WorkbookMember(
                role_id=RoleId.OWNER,
                user_id=command.user_id,
                workbook_id=new_workbook_model.id,
            )
        )
        self._session.commit()
        return WorkbookDto.model_validate(new_workbook_model)
