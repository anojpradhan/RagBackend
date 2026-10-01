import json

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

        message = {
            "role": role,
            "content": content,
        }

        self.client.rpush(
            key,
            json.dumps(message),
        )

        self.client.expire(
            key,
            60 * 60 * 24,
        )

    def get_messages(
        self,
        session_id: str,
    ) -> list[dict[str, str]]:
        key = f"chat:{session_id}"

        messages = self.client.lrange(
            key,
            0,
            -1,
        )

        return [json.loads(message) for message in messages]

    def clear_session(
        self,
        session_id: str,
    ) -> None:
        self.client.delete(f"chat:{session_id}")

        self.clear_booking_data(session_id)

    def set_booking_data(
        self,
        session_id: str,
        data: dict,
    ) -> None:
        key = f"booking:{session_id}"

        self.client.set(
            key,
            json.dumps(data),
            ex=60 * 60 * 24,
        )

    def get_booking_data(
        self,
        session_id: str,
    ) -> dict:
        key = f"booking:{session_id}"

        data = self.client.get(key)

        if not data:
            return {}

        return json.loads(data)

    def clear_booking_data(
        self,
        session_id: str,
    ) -> None:
        self.client.delete(f"booking:{session_id}")
