import uuid
from datetime import datetime
from typing import Any

import pytest

from app.models.model import Article, ArticleLike, User


def test_nested_value_to_model_creates_article_with_nested_relations():
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


def test_nested_value_checker_with_success():
    user_id = str(uuid.uuid4())

    data: dict[str, Any] = {
        "description": "Test article",
        "user_id": user_id,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
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

    Article._nested_value_checker(Article, data)  # type: ignore


def test_nested_value_checker_with_unknown_field():
    user_id = str(uuid.uuid4())

    values: dict[str, Any] = {
        "description": "Test article",
        "user_id": user_id,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "unknown_relation": {},  # 存在しないフィールド
    }

    with pytest.raises(
        ValueError, match="unknown_relation is not a valid field of Article"
    ):
        Article._nested_value_checker(Article, values)  # type: ignore
