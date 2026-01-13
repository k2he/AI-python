from motor.motor_asyncio import AsyncIOMotorClient

from app.config.config import settings
from app.config.logging_config import get_logger

logger = get_logger(__name__)


class MongoDBManager:
    def __init__(self):
        self._client: AsyncIOMotorClient = None
        self._db = None

    async def connect(self, uri: str):
        self._client = AsyncIOMotorClient(uri)
        # Automatically extracts DB name from the end of URI
        self._db = self._client.get_default_database()
        logger.info(f"Successfully connected to MongoDB: {self._db.name}")

    @property
    def db(self):
        """
        Public accessor. This is what you call from ChatRepository.
        It acts as a guard to ensure the connection exists.
        """
        if self._db is None:
            raise RuntimeError(
                "Database not initialized. Did you forget to await connect()?"
            )
        return self._db

    async def close(self):
        if self._client:
            self._client.close()
            logger.info("MongoDB connection closed.")


db_manager = MongoDBManager()
