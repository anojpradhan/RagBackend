from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.booking import BookingCreate, BookingResponse
from app.services.booking_service import BookingService

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)

booking_service = BookingService()


@router.post(
    "",
    response_model=BookingResponse,
)
async def create_booking(
    booking_data: BookingCreate,
    db: AsyncSession = Depends(get_db),
) -> BookingResponse:
    return await booking_service.create_booking(
        db,
        booking_data,
    )
