from typing import Dict

from app.schemas.user_schema import PasswordChange, TokenRefresh, UserLogin, UserRegister, UserUpdate
from app.services.auth_service import AuthService
from app.utils.response_handler import success_response


class AuthController:
    def __init__(self) -> None:
        self.service = AuthService()

    async def register(self, payload: UserRegister) -> Dict:
        return success_response(await self.service.register(payload), "User registered successfully")

    async def login(self, payload: UserLogin) -> Dict:
        return success_response(await self.service.login(payload), "Login successful")

    async def me(self, user_id: str) -> Dict:
        return success_response(await self.service.get_current_user(user_id), "Current user fetched successfully")

    async def update_profile(self, user_id: str, payload: UserUpdate) -> Dict:
        return success_response(await self.service.update_profile(user_id, payload), "Profile updated successfully")

    async def change_password(self, user_id: str, payload: PasswordChange) -> Dict:
        await self.service.change_password(user_id, payload)
        return success_response(message="Password changed successfully")

    async def refresh(self, payload: TokenRefresh) -> Dict:
        return success_response(await self.service.refresh_access_token(payload.refresh_token), "Access token refreshed successfully")
