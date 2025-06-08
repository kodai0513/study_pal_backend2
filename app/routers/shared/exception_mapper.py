from fastapi import HTTPException, status

from app.exceptions.data_not_found_exception import DataNotFoundException
from app.exceptions.resource_ownership_exception import (
    ResourceOwnershipException,
)


def map_exception_to_http(e: Exception) -> HTTPException:
    app_exception_to_http_error_handlers: dict[type, HTTPException] = {
        DataNotFoundException: HTTPException(
            status.HTTP_404_NOT_FOUND, detail=str(e)
        ),
        ResourceOwnershipException: HTTPException(
            status.HTTP_403_FORBIDDEN, detail=str(e)
        ),
    }
    for app_e, http_e in app_exception_to_http_error_handlers.items():
        if isinstance(e, app_e):
            return http_e

    # 予期しないエラーの場合
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Internal Server Error",
    )
