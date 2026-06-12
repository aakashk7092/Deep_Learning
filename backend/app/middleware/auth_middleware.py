from typing import Any, Dict

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.services.auth_service import AuthService
from app.utils.jwt_handler import decode_token
from app.utils.response_handler import unauthorized


bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme)) -> Dict[str, Any]:
    if credentials is None or credentials.scheme.lower() != "bearer":
        unauthorized("Authentication credentials were not provided")
    payload = decode_token(credentials.credentials, expected_type="access")
    return await AuthService().get_current_user(payload["sub"])


async def get_current_user_id(current_user: Dict[str, Any] = Depends(get_current_user)) -> str:
    return current_user["id"]
