from datetime import datetime

from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.book import Book
from app.models.rental import Rental
from app.models.user import User


def rent_book(
    db: Session,
    user_id: int,
    book_id: int
):
    try:
        user = db.query(User).filter(
            User.id == user_id
        ).first()

        if user is None:
            raise HTTPException(
                status_code=404,
                detail="사용자가 존재하지 않습니다."
            )

        book = (
            db.query(Book)
            .filter(Book.id == book_id)
            .with_for_update()
            .first()
        )

        if book is None:
            raise HTTPException(
                status_code=404,
                detail="도서가 존재하지 않습니다."
            )

        if book.stock <= 0:
            raise HTTPException(
                status_code=400,
                detail="대여 가능한 재고가 없습니다."
            )

        book.stock -= 1

        rental = Rental(
            user_id=user_id,
            book_id=book_id,
            rental_date=datetime.now(),
            status="RENTED"
        )

        db.add(rental)

        db.commit()

        db.refresh(rental)

        return rental

    except Exception:
        db.rollback()
        raise


def return_book(
    db: Session,
    rental_id: int
):
    try:
        rental = (
            db.query(Rental)
            .filter(Rental.id == rental_id)
            .with_for_update()
            .first()
        )

        if rental is None:
            raise HTTPException(
                status_code=404,
                detail="대여 기록이 존재하지 않습니다."
            )

        if rental.status == "RETURNED":
            raise HTTPException(
                status_code=400,
                detail="이미 반납된 도서입니다."
            )

        book = (
            db.query(Book)
            .filter(Book.id == rental.book_id)
            .with_for_update()
            .first()
        )

        if book is None:
            raise HTTPException(
                status_code=404,
                detail="도서가 존재하지 않습니다."
            )

        book.stock += 1

        rental.return_date = datetime.now()
        rental.status = "RETURNED"

        db.commit()

        db.refresh(rental)

        return rental

    except Exception:
        db.rollback()
        raise
