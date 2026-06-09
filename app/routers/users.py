from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.models.user import User

from app.schemas.user import UserCreate
from app.schemas.user import UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "",
    response_model=UserResponse
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    db_user = User(
        name=user.name,
        email=user.email
    )

    db.add(db_user)

    db.commit()

    db.refresh(db_user)

    return db_user


@router.get(
    "",
    response_model=list[UserResponse]
)
def get_users(
    db: Session = Depends(get_db)
):
    return db.query(User).all()
