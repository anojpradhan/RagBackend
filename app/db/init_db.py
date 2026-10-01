from app.db.base import Base
from app.db.database import engine
from app.models.booking import Booking


async def init_db() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)