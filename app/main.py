from fastapi import APIRouter, FastAPI

from app.routers.article import router as article_router
from app.routers.description_problem import (
    router as description_problem_router,
)
from app.routers.problem import router as problem_router

app = FastAPI()

v1 = APIRouter(prefix="/api/v1")

app.include_router(article_router)
app.include_router(description_problem_router)
app.include_router(problem_router)
