from datetime import datetime, timezone
from typing import Any, Dict, Optional

from bson import ObjectId


class UserModel:
    collection_name = "users"

    @staticmethod
    def create_document(
        full_name: str,
        email: str,
        password_hash: str,
        avatar: Optional[str] = None,
        role: str = "user",
    ) -> Dict[str, Any]:
        now = datetime.now(timezone.utc)
        return {
            "full_name": full_name,
            "email": email.lower(),
            "password_hash": password_hash,
            "avatar": avatar,
            "role": role,
            "created_at": now,
            "updated_at": now,
            "last_login": None,
        }

    @staticmethod
    def public_document(document: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "id": str(document["_id"]),
            "full_name": document["full_name"],
            "email": document["email"],
            "avatar": document.get("avatar"),
            "role": document.get("role", "user"),
            "created_at": document["created_at"],
            "updated_at": document["updated_at"],
            "last_login": document.get("last_login"),
        }

    @staticmethod
    def object_id(value: str) -> ObjectId:
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid user id")
        return ObjectId(value)
