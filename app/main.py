from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import Base
from app.database import engine

from app.models import User, Book, Rental

from app.routers.users import router as users_router
from app.routers.books import router as books_router
from app.routers.rentals import router as rentals_router
from app.routers.pages import router as pages_router

_ = (User, Book, Rental)

app = FastAPI(
    title="Library Rental System"
)

templates = Jinja2Templates(directory="app/templates")
app.state.templates = templates

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

Base.metadata.create_all(bind=engine)

app.include_router(users_router)
app.include_router(books_router)
app.include_router(rentals_router)
app.include_router(pages_router)
