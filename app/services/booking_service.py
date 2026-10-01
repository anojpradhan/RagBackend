from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.booking_repository import BookingRepository
from app.schemas.booking import BookingCreate, BookingResponse


class BookingService:
    def __init__(self) -> None:
        self.repository = BookingRepository()

    async def create_booking(
        self,
        db: AsyncSession,
        booking_data: BookingCreate,
    ) -> BookingResponse:

        booking = await self.repository.create(
            db,
            booking_data,
        )

        return BookingResponse.model_validate(booking)
