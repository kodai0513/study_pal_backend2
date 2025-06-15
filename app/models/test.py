from typing import Any

from sqlmodel import Session

from app.db.session import _engine
from app.models.model import Article

with Session(_engine) as session:
    user_id = "f2b021a4-8026-4c4d-bc23-0cf4f6cd389b"
    data: dict[str, Any] = {
        "description": "Test article",
        "user_id": user_id,
        "article_likes": [
            {
                "user_id": user_id,
            },
            {
                "user_id": user_id,
            },
        ],
    }
    Article.insert(data, session)
    session.commit()
