from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.models.book import Book
from app.models.rental import Rental
from app.models.user import User

from app.schemas.rental import RentalCreate
from app.schemas.rental import RentalListResponse
from app.schemas.rental import RentalResponse

from app.services.rental_service import rent_book
from app.services.rental_service import return_book

router = APIRouter(
    prefix="/rentals",
    tags=["Rentals"]
)


@router.post(
    "",
    response_model=RentalResponse
)
def create_rental(
    rental: RentalCreate,
    db: Session = Depends(get_db)
):
    return rent_book(
        db=db,
        user_id=rental.user_id,
        book_id=rental.book_id
    )


@router.patch(
    "/{rental_id}/return",
    response_model=RentalResponse
)
def return_rental(
    rental_id: int,
    db: Session = Depends(get_db)
):
    return return_book(
        db=db,
        rental_id=rental_id
    )


@router.get(
    "",
    response_model=list[RentalListResponse]
)
def get_rentals(
    db: Session = Depends(get_db)
):
    rentals = (
        db.query(
            Rental.id.label("rental_id"),
            User.name.label("user_name"),
            Book.title.label("book_title"),
            Rental.rental_date,
            Rental.return_date,
            Rental.status
        )
        .join(User, Rental.user_id == User.id)
        .join(Book, Rental.book_id == Book.id)
        .order_by(Rental.rental_date.desc())
        .all()
    )

    return rentals
