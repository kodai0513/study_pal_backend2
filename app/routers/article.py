from fastapi import APIRouter, status

from app.db.session import SessionDep
from app.middlewares.auth import AuthDep
from app.routers.shared.exception_mapper import map_exception_to_http
from app.schemas.article import (
    ArticleResp,
    CreateArticleReq,
    UpdateArticleReq,
)
from app.usecases.articles.create import CreateAction, CreateCommand
from app.usecases.articles.delete import DeleteAction, DeleteCommand
from app.usecases.articles.update import UpdateAction, UpdateCommand

router = APIRouter(prefix="/articles")


@router.post(
    "/", response_model=ArticleResp, status_code=status.HTTP_201_CREATED
)
def create_article(
    req: CreateArticleReq, session: SessionDep, auth: AuthDep
) -> ArticleResp:
    try:
        return ArticleResp.model_validate(
            CreateAction(session).execute(
                CreateCommand(
                    **req.model_dump(),
                    user_id=auth.user_id,
                )
            )
        )
    except Exception as e:
        raise map_exception_to_http(e)


@router.patch(
    "/{article_id}",
    response_model=ArticleResp,
    status_code=status.HTTP_200_OK,
)
def update_article(
    article_id: str, req: UpdateArticleReq, session: SessionDep, auth: AuthDep
) -> ArticleResp:
    try:
        return ArticleResp.model_validate(
            UpdateAction(session).execute(
                UpdateCommand(
                    **req.model_dump(),
                    user_id=auth.user_id,
                    article_id=article_id,
                )
            )
        )
    except Exception as e:
        raise map_exception_to_http(e)


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(
    article_id: str, session: SessionDep, auth: AuthDep
) -> None:
    try:
        DeleteAction(session).execute(
            DeleteCommand(article_id=article_id, user_id=auth.user_id)
        )

        return
    except Exception as e:
        raise map_exception_to_http(e)
