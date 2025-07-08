from fastapi import APIRouter, status

from app.db.session import SessionDep
from app.middlewares.auth import AuthDep
from app.routers.shared.exception_mapper import map_exception_to_http
from app.schemas.pages.timeline import TimelineResp
from app.schemas.shared.page_info import PageInfo
from app.usecases.timelines.index import IndexAction, IndexCommand

router = APIRouter()


@router.get(
    "/timelines",
    response_model=TimelineResp,
    status_code=status.HTTP_200_OK,
)
def index(
    session: SessionDep,
    auth: AuthDep,
    next_page_token: str | None = None,
    page_size: int = 20,
    prev_page_token: str | None = None,
) -> TimelineResp:
    try:
        return TimelineResp.model_validate(
            IndexAction(session).execute(
                IndexCommand(
                    page_info=PageInfo(
                        next_page_token=next_page_token,
                        page_size=page_size,
                        prev_page_token=prev_page_token,
                    )
                )
            )
        )
    except Exception as e:
        raise map_exception_to_http(e)
