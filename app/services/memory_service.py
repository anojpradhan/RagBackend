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

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
    ) -> None:

        key = f"chat:{session_id}"

        self.client.rpush(
            key,
            f"{role}:{content}",
        )

    def get_messages(
        self,
        session_id: str,
    ) -> list[str]:

        key = f"chat:{session_id}"

        return self.client.lrange(
            key,
            0,
            -1,
        )
