from fastapi import APIRouter, status

from app.db.session import SessionDep
from app.middlewares.auth import AuthDep
from app.routers.shared.exception_mapper import map_exception_to_http
from app.schemas.selection_problem import (
    SelectionProblemResp,
    UpdateSelectionProblemReq,
)
from app.usecases.selection_problems.delete import (
    DeleteAction,
    DeleteCommand,
)
from app.usecases.selection_problems.update import (
    UpdateAction,
    UpdateCommand,
)

router = APIRouter(
    prefix=(
        "/workbooks/{workbook_id}/selection-problems/" "{selection_problem_id}"
    )
)


@router.put(
    "",
    response_model=SelectionProblemResp,
    status_code=status.HTTP_200_OK,
)
def update(
    selection_problem_id: str,
    workbook_id: str,
    req: UpdateSelectionProblemReq,
    session: SessionDep,
    auth: AuthDep,
) -> SelectionProblemResp:
    try:
        return SelectionProblemResp.model_validate(
            UpdateAction(session).execute(
                UpdateCommand(
                    **req.model_dump(),
                    selection_problem_id=selection_problem_id,
                    workbook_id=workbook_id
                )
            )
        )
    except Exception as e:
        raise map_exception_to_http(e)


@router.delete(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete(
    selection_problem_id: str,
    workbook_id: str,
    session: SessionDep,
    auth: AuthDep,
) -> None:
    try:
        DeleteAction(session).execute(
            DeleteCommand(
                selection_problem_id=selection_problem_id,
                workbook_id=workbook_id,
            )
        )

        return
    except Exception as e:
        raise map_exception_to_http(e)
