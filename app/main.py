from fastapi import APIRouter, FastAPI

from app.routers.article import router as article_router

app = FastAPI()

v1 = APIRouter(prefix="/api/v1")

app.include_router(article_router)
