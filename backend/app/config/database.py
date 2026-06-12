import logging
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import ASCENDING, DESCENDING

from app.config.settings import get_settings


logger = logging.getLogger(__name__)


class MongoDatabase:
    client: Optional[AsyncIOMotorClient] = None
    database: Optional[AsyncIOMotorDatabase] = None


db = MongoDatabase()


async def connect_to_mongo() -> None:
    settings = get_settings()
    db.client = AsyncIOMotorClient(settings.mongodb_uri, uuidRepresentation="standard")
    db.database = db.client[settings.database_name]
    await db.database.command("ping")
    await create_indexes(db.database)
    logger.info("Connected to MongoDB database '%s'", settings.database_name)


async def close_mongo_connection() -> None:
    if db.client:
        db.client.close()
        logger.info("MongoDB connection closed")


def get_database() -> AsyncIOMotorDatabase:
    if db.database is None:
        raise RuntimeError("Database is not initialized")
    return db.database


async def create_indexes(database: AsyncIOMotorDatabase) -> None:
    await database.users.create_index([("email", ASCENDING)], unique=True)
    await database.users.create_index([("created_at", DESCENDING)])
    await database.predictions.create_index([("user_id", ASCENDING), ("created_at", DESCENDING)])
    await database.predictions.create_index([("disease_name", ASCENDING)])
    await database.diseases.create_index([("plant_name", ASCENDING), ("disease_name", ASCENDING)], unique=True)


def users_collection():
    return get_database().users


def predictions_collection():
    return get_database().predictions


def diseases_collection():
    return get_database().diseases
