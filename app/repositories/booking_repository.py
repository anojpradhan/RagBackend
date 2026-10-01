from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Booking
from app.schemas.booking import BookingCreate


class BookingRepository:
    async def create(
        self,
        db: AsyncSession,
        booking_data: BookingCreate,
    ) -> Booking:
        booking = Booking(
            name=booking_data.name,
            email=booking_data.email,
            interview_date=booking_data.interview_date,
            interview_time=booking_data.interview_time,
        )

        db.add(booking)

        await db.commit()
        await db.refresh(booking)

        return booking
