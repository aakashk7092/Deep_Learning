from typing import Any, Dict, Optional

from fastapi import HTTPException, status


def success_response(data: Any = None, message: str = "Success") -> Dict[str, Any]:
    return {"success": True, "message": message, "data": data}


def raise_http_error(status_code: int, message: str, detail: Optional[Any] = None) -> None:
    raise HTTPException(
        status_code=status_code,
        detail={"success": False, "message": message, "detail": detail},
    )


def bad_request(message: str, detail: Optional[Any] = None) -> None:
    raise_http_error(status.HTTP_400_BAD_REQUEST, message, detail)


def unauthorized(message: str = "Unauthorized", detail: Optional[Any] = None) -> None:
    raise_http_error(status.HTTP_401_UNAUTHORIZED, message, detail)


def forbidden(message: str = "Forbidden", detail: Optional[Any] = None) -> None:
    raise_http_error(status.HTTP_403_FORBIDDEN, message, detail)


def not_found(message: str = "Resource not found", detail: Optional[Any] = None) -> None:
    raise_http_error(status.HTTP_404_NOT_FOUND, message, detail)


def conflict(message: str, detail: Optional[Any] = None) -> None:
    raise_http_error(status.HTTP_409_CONFLICT, message, detail)
