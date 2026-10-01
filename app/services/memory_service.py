import redis

from app.core.config import settings


class MemoryService:
    def __init__(self) -> None:
        self.client = redis.Redis.from_url(
            settings.redis_url,
            decode_responses=True,
        )

    def ping(self) -> bool:
        return self.client.ping()
