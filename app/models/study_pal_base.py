from datetime import datetime
from typing import Any, Type, TypeVar

import uuid6
from sqlmodel import CHAR, Field, SQLModel, select

from app.db.session import SessionDep

T = TypeVar("T", bound="StudyPalBaseModel")

MYSQL_UUID = CHAR(36)


class StudyPalBaseModel(SQLModel):
    id: str = Field(
        default_factory=uuid6.uuid7,
        sa_type=MYSQL_UUID,  # type: ignore
        primary_key=True,
    )

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(
        default_factory=datetime.now,
        sa_column_kwargs={"onupdate": datetime.now},
    )

    @classmethod
    def update_or_insert(
        cls: Type[T],
        model: T,
        session: SessionDep,
        update_values: dict[str, Any] | None = None,
    ) -> T:

        if update_values is not None:
            for key, value in update_values.items():
                if hasattr(model, key):
                    setattr(model, key, value)
                else:
                    raise ValueError(
                        f"{key} is not a valid field of {cls.__name__}"
                    )

        session.add(model)
        update_model = session.exec(
            select(cls).where(cls.id == model.id)
        ).one()

        return update_model

    @classmethod
    def delete(
        cls: Type[T],
        model: T,
        session: SessionDep,
    ) -> None:
        session.delete(model)
