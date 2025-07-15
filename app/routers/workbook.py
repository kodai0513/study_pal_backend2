from fastapi import APIRouter, status

from app.db.session import SessionDep
from app.middlewares.auth import AuthDep
from app.routers.shared.exception_mapper import map_exception_to_http
from app.schemas.resources.workbook import (
    CreateWorkbookReq,
    UpdateWorkbookReq,
    WorkbookResp,
)
from app.schemas.shared.page_info import PageInfo
from app.schemas.views.workbook import WorkbookListViewResp
from app.usecases.workbook_me.workbook_me import (
    WorkbookMeAction,
    WorkbookMeCommand,
)
from app.usecases.workbook_search.workbook_search import (
    WorkbookSearchAction,
    WorkbookSearchCommand,
)
from app.usecases.workbooks.create import CreateAction, CreateCommand
from app.usecases.workbooks.delete import DeleteAction, DeleteCommand
from app.usecases.workbooks.update import UpdateAction, UpdateCommand

router = APIRouter(prefix="/workbooks")


@router.get(
    "/me", response_model=WorkbookListViewResp, status_code=status.HTTP_200_OK
)
def get_workbooks_for_me(
    session: SessionDep,
    auth: AuthDep,
    next_page_token: str | None = None,
    page_size: int = 20,
) -> WorkbookListViewResp:
    try:
        return WorkbookListViewResp.model_validate(
            WorkbookMeAction(session).execute(
                WorkbookMeCommand(
                    authUser=auth,
                    page_info=PageInfo(
                        next_page_token=next_page_token,
                        page_size=page_size,
                    ),
                )
            )
        )
    except Exception as e:
        raise map_exception_to_http(e)


@router.get(
    "/", response_model=WorkbookListViewResp, status_code=status.HTTP_200_OK
)
def get_workbooks_by_keyword(
    session: SessionDep,
    keyword: str = "",
    next_page_token: str | None = None,
    page_size: int = 20,
) -> WorkbookListViewResp:
    try:
        return WorkbookListViewResp.model_validate(
            WorkbookSearchAction(session).execute(
                WorkbookSearchCommand(
                    keyword=keyword,
                    page_info=PageInfo(
                        next_page_token=next_page_token,
                        page_size=page_size,
                    ),
                )
            )
        )
    except Exception as e:
        raise map_exception_to_http(e)


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
