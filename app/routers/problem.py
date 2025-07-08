from fastapi import APIRouter, status

from app.db.session import SessionDep
from app.middlewares.auth import AuthDep
from app.routers.shared.exception_mapper import map_exception_to_http
from app.schemas.resources.problem import CreateProblemReq, ProblemResp
from app.usecases.problems.create import CreateAction, CreateCommand

router = APIRouter()


@router.post(
    "/problems/{workbook_id}",
    response_model=ProblemResp,
    status_code=status.HTTP_201_CREATED,
)
def create(
    workbook_id: str, req: CreateProblemReq, session: SessionDep, auth: AuthDep
) -> ProblemResp:
    try:
        return ProblemResp.model_validate(
            CreateAction(session).execute(
                CreateCommand(
                    **req.model_dump(),
                    user_id=auth.user_id,
                    workbook_id=workbook_id
                )
            )
        )
    except Exception as e:
        raise map_exception_to_http(e)
