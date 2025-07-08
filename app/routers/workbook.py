from fastapi import APIRouter, status

from app.db.session import SessionDep
from app.middlewares.auth import AuthDep
from app.routers.shared.exception_mapper import map_exception_to_http
from app.schemas.resources.workbook import (
    CreateWorkbookReq,
    UpdateWorkbookReq,
    WorkbookResp,
)
from app.usecases.workbooks.create import CreateAction, CreateCommand
from app.usecases.workbooks.delete import DeleteAction, DeleteCommand
from app.usecases.workbooks.update import UpdateAction, UpdateCommand

router = APIRouter(prefix="/workbooks")


@router.post(
    "/", response_model=WorkbookResp, status_code=status.HTTP_201_CREATED
)
def create(
    req: CreateWorkbookReq, session: SessionDep, auth: AuthDep
) -> WorkbookResp:
    try:
        return WorkbookResp.model_validate(
            CreateAction(session).execute(
                CreateCommand(
                    **req.model_dump(),
                    user_id=auth.user_id,
                )
            )
        )
    except Exception as e:
        raise map_exception_to_http(e)


@router.put(
    "/{workbook_id}",
    response_model=WorkbookResp,
    status_code=status.HTTP_200_OK,
)
def update(
    workbook_id: str,
    req: UpdateWorkbookReq,
    session: SessionDep,
    auth: AuthDep,
) -> WorkbookResp:
    try:
        return WorkbookResp.model_validate(
            UpdateAction(session).execute(
                UpdateCommand(
                    **req.model_dump(),
                    user_id=auth.user_id,
                    workbook_id=workbook_id,
                )
            )
        )
    except Exception as e:
        raise map_exception_to_http(e)


@router.delete("/{workbook_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(workbook_id: str, session: SessionDep, auth: AuthDep) -> None:
    try:
        DeleteAction(session).execute(
            DeleteCommand(workbook_id=workbook_id, user_id=auth.user_id)
        )

        return
    except Exception as e:
        raise map_exception_to_http(e)
