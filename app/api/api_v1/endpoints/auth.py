from fastapi import APIRouter, Body, Depends, HTTPException, status
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

from app import crud, models, schemas
from app.core.config import settings
from app.core import security
from app.api import dependencies


router = APIRouter()


@router.post("/register", response_model=schemas.User)
def register(*, db=Depends(dependencies.get_db), user_in: schemas.UserCreate):
    """Create new user.
    This endpoint is used to create a new user.
    Args:
        user_in (schemas.UserCreate): User object to be created.
    Returns:
        schemas.User: Created user object.
    Raises:
        HTTPException: 400 if email already registered.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email {user_in.email} already registered",
        )
    user = crud.user.create(db=db, obj_in=user_in)
    return user


@router.post("/login", response_model=schemas.Token)
def login(
    *, db=Depends(dependencies.get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """Login user.
    This endpoint is used to login a user.
    Args:
        form_data (OAuth2PasswordRequestForm): User credentials.
    Returns:
        schemas.Token: User token.
    Raises:
        HTTPException: 401 if user not found or password incorrect.
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    elif not crud.user.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "Bearer",
    }
