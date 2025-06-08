from fastapi import APIRouter, status

from app.db.session import SessionDep
from app.middlewares.auth import AuthDep
from app.routers.shared.exception_mapper import map_exception_to_http
from app.schemas.problem import CreateProblemReq, ProblemResp
from app.usecases.articles.create import CreateAction, CreateCommand

router = APIRouter(prefix="/problems")


@router.post(
    "/", response_model=ProblemResp, status_code=status.HTTP_201_CREATED
)
def create_article(
    req: CreateProblemReq, session: SessionDep, auth: AuthDep
) -> ProblemResp:
    try:
        return ProblemResp.model_validate(
            CreateAction(session).execute(
                CreateCommand(**req.model_dump(), user_id=auth.user_id)
            )
        )
    except Exception as e:
        raise map_exception_to_http(e)
