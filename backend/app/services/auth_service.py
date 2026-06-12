from datetime import datetime, timezone
from typing import Any, Dict

from bson import ObjectId
from passlib.context import CryptContext
from pymongo.errors import DuplicateKeyError

from app.config.database import users_collection
from app.models.User import UserModel
from app.schemas.user_schema import PasswordChange, UserLogin, UserRegister, UserUpdate
from app.utils.jwt_handler import create_access_token, create_refresh_token, decode_token
from app.utils.response_handler import bad_request, conflict, not_found, unauthorized


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, password_hash: str) -> bool:
        return pwd_context.verify(plain_password, password_hash)

    async def register(self, payload: UserRegister) -> Dict[str, Any]:
        document = UserModel.create_document(
            full_name=payload.full_name,
            email=str(payload.email),
            password_hash=self.hash_password(payload.password),
            avatar=payload.avatar,
        )
        try:
            result = await users_collection().insert_one(document)
        except DuplicateKeyError:
            conflict("Email is already registered")

        created = await users_collection().find_one({"_id": result.inserted_id})
        return self._auth_payload(created)

    async def login(self, payload: UserLogin) -> Dict[str, Any]:
        user = await users_collection().find_one({"email": str(payload.email).lower()})
        if not user or not self.verify_password(payload.password, user["password_hash"]):
            unauthorized("Invalid email or password")

        await users_collection().update_one(
            {"_id": user["_id"]},
            {"$set": {"last_login": datetime.now(timezone.utc), "updated_at": datetime.now(timezone.utc)}},
        )
        user = await users_collection().find_one({"_id": user["_id"]})
        return self._auth_payload(user)

    async def refresh_access_token(self, refresh_token: str) -> Dict[str, str]:
        payload = decode_token(refresh_token, expected_type="refresh")
        user = await self.get_user_document(payload["sub"])
        access_token = create_access_token(str(user["_id"]), {"role": user.get("role", "user")})
        return {"access_token": access_token, "token_type": "bearer"}

    async def get_current_user(self, user_id: str) -> Dict[str, Any]:
        user = await self.get_user_document(user_id)
        return UserModel.public_document(user)

    async def update_profile(self, user_id: str, payload: UserUpdate) -> Dict[str, Any]:
        update_data = {key: value for key, value in payload.model_dump(exclude_unset=True).items() if value is not None}
        if not update_data:
            bad_request("No profile fields were provided")
        update_data["updated_at"] = datetime.now(timezone.utc)
        user = await self.get_user_document(user_id)
        await users_collection().update_one({"_id": user["_id"]}, {"$set": update_data})
        updated = await users_collection().find_one({"_id": user["_id"]})
        return UserModel.public_document(updated)

    async def change_password(self, user_id: str, payload: PasswordChange) -> None:
        user = await self.get_user_document(user_id)
        if not self.verify_password(payload.current_password, user["password_hash"]):
            unauthorized("Current password is incorrect")
        await users_collection().update_one(
            {"_id": user["_id"]},
            {"$set": {"password_hash": self.hash_password(payload.new_password), "updated_at": datetime.now(timezone.utc)}},
        )

    async def get_user_document(self, user_id: str) -> Dict[str, Any]:
        if not ObjectId.is_valid(user_id):
            unauthorized("Invalid user token")
        user = await users_collection().find_one({"_id": ObjectId(user_id)})
        if not user:
            not_found("User not found")
        return user

    @staticmethod
    def _auth_payload(user: Dict[str, Any]) -> Dict[str, Any]:
        user_id = str(user["_id"])
        public_user = UserModel.public_document(user)
        return {
            "user": public_user,
            "access_token": create_access_token(user_id, {"role": public_user["role"]}),
            "refresh_token": create_refresh_token(user_id),
            "token_type": "bearer",
        }
