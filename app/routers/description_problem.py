from fastapi import APIRouter, status

from app.db.session import SessionDep
from app.middlewares.auth import AuthDep
from app.routers.shared.exception_mapper import map_exception_to_http
from app.schemas.description_problem import (
    DescriptionProblemResp,
    UpdateDescriptionProblemReq,
)
from app.usecases.description_problems.delete import (
    DeleteAction,
    DeleteCommand,
)
from app.usecases.description_problems.update import (
    UpdateAction,
    UpdateCommand,
)

router = APIRouter(
    prefix=(
        "/workbooks/{workbook_id}/description-problems/"
        "{description_problem_id}"
    )
)


@router.put(
    "",
    response_model=DescriptionProblemResp,
    status_code=status.HTTP_200_OK,
)
def update(
    description_problem_id: str,
    workbook_id: str,
    req: UpdateDescriptionProblemReq,
    session: SessionDep,
    auth: AuthDep,
) -> DescriptionProblemResp:
    try:
        return DescriptionProblemResp.model_validate(
            UpdateAction(session).execute(
                UpdateCommand(
                    **req.model_dump(),
                    description_problem_id=description_problem_id,
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
    description_problem_id: str,
    workbook_id: str,
    session: SessionDep,
    auth: AuthDep,
) -> None:
    try:
        DeleteAction(session).execute(
            DeleteCommand(
                description_problem_id=description_problem_id,
                workbook_id=workbook_id,
            )
        )

        return
    except Exception as e:
        raise map_exception_to_http(e)
