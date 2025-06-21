import uuid
from datetime import datetime
from typing import Any

import pytest

from app.models.model import Article, ArticleLike, User
from app.models.study_pal_base import Operation


def test_nested_value_to_model_正常に動作するか():
    user_id = str(uuid.uuid4())
    data: dict[str, Any] = {
        "description": "Test article",
        "user_id": user_id,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "user": {
            "id": user_id,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        },
        "article_likes": [
            {
                "user_id": user_id,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            },
            {
                "user_id": user_id,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            },
        ],
    }

    article = Article._nested_value_to_model(Article, data)  # type: ignore

    assert isinstance(article, Article)
    assert article.description == "Test article"
    assert article.user is not None
    assert isinstance(article.user, User)
    assert len(article.article_likes) == 2
    assert isinstance(article.article_likes[0], ArticleLike)
    assert isinstance(article.article_likes[1], ArticleLike)


def test_nested_value_checker_正常系_INSERT_ネストあり():
    user_id = str(uuid.uuid4())
    data: dict[str, Any] = {
        "description": "Test article",
        "user_id": user_id,
        "article_likes": [
            {
                "user_id": user_id,
            }
        ],
    }

    # INSERT はネストされたリレーションが許容される
    Article._nested_value_checker(  # type: ignore
        Article, Operation.INSERT, data
    )


def test_nested_value_checker_UPDATEでネストされたdictを含むとエラー():
    user_id = str(uuid.uuid4())
    data: dict[str, Any] = {
        "description": "Updated article",
        "user_id": user_id,
        "user": {
            "id": user_id,
        },
    }

    with pytest.raises(
        ValueError,
        match=r"Cannot include nested relation 'user' in update operation",
    ):
        Article._nested_value_checker(  # type: ignore
            Article, Operation.UPDATE, data
        )


def test_nested_value_checker_UPDATEでネストされたlistを含むとエラー():
    user_id = str(uuid.uuid4())
    data: dict[str, Any] = {
        "description": "Updated article",
        "user_id": user_id,
        "article_likes": [{"user_id": user_id}],
    }

    with pytest.raises(
        ValueError,
        match=(
            r"Cannot include nested relation 'article_likes' in update "
            r"operation"
        ),
    ):
        Article._nested_value_checker(  # type: ignore
            Article, Operation.UPDATE, data
        )


def test_nested_value_checker_不明なフィールドを含むとエラー():
    user_id = str(uuid.uuid4())
    data: dict[str, Any] = {
        "description": "Article",
        "user_id": user_id,
        "unknown_field": 123,
    }

    with pytest.raises(
        ValueError, match=r"unknown_field is not a valid field of Article"
    ):
        Article._nested_value_checker(  # type: ignore
            Article, Operation.INSERT, data
        )
