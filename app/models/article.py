import uuid
from typing import Optional

from sqlmodel import Column, Field, Integer, Relationship

from app.models.base import Base


class Article(Base, table=True):
    page_id: int | None = Field(
        default=None,
        sa_column=Column(
            Integer, autoincrement=True, nullable=True, unique=True
        ),
    )
    description: str = Field(max_length=400)
    user_id: uuid.UUID = Field(foreign_key="user.id")

    user: Optional["User"] = Relationship(back_populates="articles")
