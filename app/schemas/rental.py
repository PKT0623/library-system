from datetime import datetime

from pydantic import BaseModel


class RentalCreate(BaseModel):
    user_id: int
    book_id: int


class RentalResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    rental_date: datetime
    return_date: datetime | None
    status: str

    model_config = {
        "from_attributes": True
    }


class RentalListResponse(BaseModel):
    rental_id: int
    user_name: str
    book_title: str
    rental_date: datetime
    return_date: datetime | None
    status: str
