from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.models.book import Book

from app.schemas.book import BookCreate
from app.schemas.book import BookResponse

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


@router.post(
    "",
    response_model=BookResponse
)
def create_book(
    book: BookCreate,
    db: Session = Depends(get_db)
):
    db_book = Book(
        title=book.title,
        author=book.author,
        stock=book.stock
    )

    db.add(db_book)

    db.commit()

    db.refresh(db_book)

    return db_book


@router.get(
    "",
    response_model=list[BookResponse]
)
def get_books(
    db: Session = Depends(get_db)
):
    return db.query(Book).all()
