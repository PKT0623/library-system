from datetime import datetime

from pydantic import BaseModel
from pydantic import Field


class BookCreate(BaseModel):
    title: str
    author: str
    stock: int = Field(ge=0)


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    stock: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
