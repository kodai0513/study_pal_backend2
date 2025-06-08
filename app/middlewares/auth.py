from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, HTTPException, status


@dataclass
class AuthInfo:
    user_id: str
    user_name: str


def _auth_required() -> AuthInfo:
    # 実際はトークン検証などを行う
    authorized = True  # ここを切り替えてテストできる
    if not authorized:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    return AuthInfo(
        user_id="f2b021a4-8026-4c4d-bc23-0cf4f6cd389b", user_name="admin"
    )


AuthDep = Annotated[AuthInfo, Depends(_auth_required)]
