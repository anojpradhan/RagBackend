from datetime import date, time
from uuid import UUID

from pydantic import BaseModel, EmailStr


class BookingCreate(BaseModel):
    name: str
    email: EmailStr
    interview_date: date
    interview_time: time


class BookingResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    interview_date: date
    interview_time: time

    model_config = {
        "from_attributes": True,
    }
