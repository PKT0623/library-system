from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import Request
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.book import Book
from app.models.rental import Rental
from app.models.user import User
from app.services.rental_service import rent_book
from app.services.rental_service import return_book

router = APIRouter(
    tags=["Pages"]
)


@router.get("/")
def books_page(
    request: Request,
    db: Session = Depends(get_db)
):
    books = db.query(Book).order_by(Book.id).all()
    users = db.query(User).order_by(User.id).all()

    return request.app.state.templates.TemplateResponse(
        request=request,
        name="books.html",
        context={
            "books": books,
            "users": users
        }
    )


@router.get("/admin")
def admin_page(
    request: Request,
    db: Session = Depends(get_db)
):
    users = db.query(User).order_by(User.id).all()
    books = db.query(Book).order_by(Book.id).all()

    return request.app.state.templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={
            "users": users,
            "books": books
        }
    )


@router.post("/admin/users")
def create_user_page(
    name: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    user = User(
        name=name,
        email=email
    )

    db.add(user)
    db.commit()

    return RedirectResponse(
        url="/admin",
        status_code=303
    )


@router.post("/admin/books")
def create_book_page(
    title: str = Form(...),
    author: str = Form(...),
    stock: int = Form(...),
    db: Session = Depends(get_db)
):
    book = Book(
        title=title,
        author=author,
        stock=stock
    )

    db.add(book)
    db.commit()

    return RedirectResponse(
        url="/admin",
        status_code=303
    )


@router.post("/rentals-page")
def rent_book_page(
    user_id: int = Form(...),
    book_id: int = Form(...),
    db: Session = Depends(get_db)
):
    rent_book(
        db=db,
        user_id=user_id,
        book_id=book_id
    )

    return RedirectResponse(
        url="/",
        status_code=303
    )


@router.get("/rentals-page")
def rentals_page(
    request: Request,
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

    return request.app.state.templates.TemplateResponse(
        request=request,
        name="rentals.html",
        context={
            "rentals": rentals
        }
    )


@router.post("/rentals-page/{rental_id}/return")
def return_book_page(
    rental_id: int,
    db: Session = Depends(get_db)
):
    return_book(
        db=db,
        rental_id=rental_id
    )

    return RedirectResponse(
        url="/rentals-page",
        status_code=303
    )
