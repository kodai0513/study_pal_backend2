from collections import defaultdict
from datetime import datetime
from enum import Enum
from typing import Any, DefaultDict, TypeVar, cast, get_type_hints

import uuid6
from sqlalchemy import or_
from sqlmodel import CHAR, Field, SQLModel, delete, select
from sqlmodel import update as sql_update

from app.db.session import SessionDep
from app.models.study_pal_base_model_analyzer import StudyPalBaseModelAnalyzer

T = TypeVar("T", bound="StudyPalBaseModel")

MYSQL_UUID = CHAR(36)


class Operation(Enum):
    INSERT = "insert"
    UPDATE = "update"


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
    def _nested_value_checker(
        cls, mold: type, operation: Operation, values: dict[str, Any]
    ) -> None:
        type_hints = get_type_hints(mold)

        for key, value in values.items():
            if key not in type_hints:
                raise ValueError(
                    f"{key} is not a valid field of {mold.__name__}"
                )
            if operation == Operation.UPDATE and (
                isinstance(value, list) or isinstance(value, dict)
            ):
                raise ValueError(
                    f"Cannot include nested relation '{key}' in update operation. "  # noqa
                    "Please update related records separately."
                )
            # リレーションに対する対応
            if isinstance(value, list):
                child_mold = (
                    StudyPalBaseModelAnalyzer.get_related_model_type_from_list(
                        key, mold
                    )
                )
                for v in cast(list[dict[str, Any]], value):
                    cls._nested_value_checker(child_mold, operation, v)
            if isinstance(value, dict):
                child_mold = StudyPalBaseModelAnalyzer.get_related_model_type(
                    key, mold
                )
                cls._nested_value_checker(
                    child_mold, operation, cast(dict[str, Any], value)
                )

            if key == "id":
                raise ValueError(
                    f"{key} is not a valid field of {mold.__name__}"
                )

    @classmethod
    def _nested_value_to_model(
        cls, parent_mold: type, values: dict[str, Any]
    ) -> object:
        model_args: DefaultDict[str, Any] = defaultdict(list)
        for key, value in values.items():
            # リレーションに対する対応
            if isinstance(value, list):
                child_mold = (
                    StudyPalBaseModelAnalyzer.get_related_model_type_from_list(
                        key, parent_mold
                    )
                )
                for v in cast(list[dict[str, Any]], value):
                    cast(list[object], model_args[key]).append(
                        cls._nested_value_to_model(child_mold, v)
                    )
            elif isinstance(value, dict):
                child_mold = StudyPalBaseModelAnalyzer.get_related_model_type(
                    key, parent_mold
                )
                model_args[key] = cls._nested_value_to_model(
                    child_mold, cast(dict[str, Any], value)
                )
            else:
                model_args[key] = value

        return parent_mold(**model_args)

    @classmethod
    def insert(
        cls: type[T],
        insert_values: dict[str, Any],
        session: SessionDep,
    ) -> T:
        cls._nested_value_checker(cls, Operation.INSERT, insert_values)
        new_model = cls._nested_value_to_model(cls, insert_values)
        session.add(new_model)
        session.flush()

        return cast(T, new_model)

    @classmethod
    def update_by_id(
        cls: type[T],
        id: str,
        session: SessionDep,
        update_values: dict[str, Any],
    ) -> T:
        cls._nested_value_checker(cls, Operation.UPDATE, update_values)
        session.exec(
            sql_update(cls)
            .where(cls.id == id)  # type: ignore
            .values(**update_values)
        )

        return session.exec(select(cls).where(cls.id == id)).one()

    @classmethod
    def bulk_insert(
        cls: type[T],
        bulk_insert_values: list[dict[str, Any]],
        session: SessionDep,
    ) -> list[T]:
        for v in bulk_insert_values:
            cls._nested_value_checker(cls, Operation.INSERT, v)

        models = [
            cls._nested_value_to_model(cls, v) for v in bulk_insert_values
        ]
        session.add_all(models)
        session.flush()

        return cast(list[T], models)

    @classmethod
    def delete(
        cls: type[T],
        model: T,
        session: SessionDep,
    ) -> None:
        session.delete(model)

    @classmethod
    def delete_by_ids(
        cls: type[T], ids: list[str], session: SessionDep
    ) -> None:
        if len(ids) == 0:
            return

        stmt = delete(cls).where(
            or_(*[cls.id == id for id in ids])  # type: ignore
        )
        session.exec(stmt)  # type: ignore
