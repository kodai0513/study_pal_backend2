from fastapi import APIRouter, status

from app.db.session import SessionDep
from app.middlewares.auth import AuthDep
from app.routers.shared.exception_mapper import map_exception_to_http
from app.schemas.resources.true_or_false_problem import (
    TrueOrFalseProblemResp,
    UpdateTrueOrFalseProblemReq,
)
from app.usecases.true_or_false_problems.delete import (
    DeleteAction,
    DeleteCommand,
)
from app.usecases.true_or_false_problems.update import (
    UpdateAction,
    UpdateCommand,
)

router = APIRouter(
    prefix=(
        "/workbooks/{workbook_id}/true-or-false-problems/"
        "{true_or_false_problem_id}"
    )
)


@router.put(
    "",
    response_model=TrueOrFalseProblemResp,
    status_code=status.HTTP_200_OK,
)
def update(
    true_or_false_problem_id: str,
    workbook_id: str,
    req: UpdateTrueOrFalseProblemReq,
    session: SessionDep,
    auth: AuthDep,
) -> TrueOrFalseProblemResp:
    try:
        return TrueOrFalseProblemResp.model_validate(
            UpdateAction(session).execute(
                UpdateCommand(
                    **req.model_dump(),
                    true_or_false_problem_id=true_or_false_problem_id,
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
    true_or_false_problem_id: str,
    workbook_id: str,
    session: SessionDep,
    auth: AuthDep,
) -> None:
    try:
        DeleteAction(session).execute(
            DeleteCommand(
                true_or_false_problem_id=true_or_false_problem_id,
                workbook_id=workbook_id,
            )
        )

        return
    except Exception as e:
        raise map_exception_to_http(e)
