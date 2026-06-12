from fastapi import APIRouter, Depends, status

from app.controllers.auth_controller import AuthController
from app.middleware.auth_middleware import get_current_user_id
from app.schemas.user_schema import PasswordChange, TokenRefresh, UserLogin, UserRegister, UserUpdate


router = APIRouter(prefix="/api/auth", tags=["Authentication"])
controller = AuthController()


@router.post("/register", status_code=status.HTTP_201_CREATED, summary="Register a new user")
async def register(payload: UserRegister):
    return await controller.register(payload)


@router.post("/login", summary="Login and receive JWT tokens")
async def login(payload: UserLogin):
    return await controller.login(payload)


@router.post("/refresh", summary="Refresh an access token")
async def refresh(payload: TokenRefresh):
    return await controller.refresh(payload)


@router.get("/me", summary="Get current authenticated user")
async def me(user_id: str = Depends(get_current_user_id)):
    return await controller.me(user_id)


@router.put("/profile", summary="Update current user profile")
async def update_profile(payload: UserUpdate, user_id: str = Depends(get_current_user_id)):
    return await controller.update_profile(user_id, payload)


@router.put("/change-password", summary="Change current user password")
async def change_password(payload: PasswordChange, user_id: str = Depends(get_current_user_id)):
    return await controller.change_password(user_id, payload)
