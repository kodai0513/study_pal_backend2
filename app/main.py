from fastapi import APIRouter, FastAPI

from app.routers.article import router as article_router
from app.routers.description_problem import (
    router as description_problem_router,
)
from app.routers.problem import router as problem_router
from app.routers.selection_problem import router as selection_problem_router
from app.routers.true_or_false_problem import (
    router as true_or_false_problem_router,
)
from app.routers.workbook import router as workbook_router

app = FastAPI()

v1 = APIRouter(prefix="/api/v1")

app.include_router(article_router)
app.include_router(description_problem_router)
app.include_router(problem_router)
app.include_router(selection_problem_router)
app.include_router(true_or_false_problem_router)
app.include_router(workbook_router)
