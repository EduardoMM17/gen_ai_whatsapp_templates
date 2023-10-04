from fastapi import APIRouter, Body, Depends, HTTPException, status
from app import crud, models, schemas
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
    print("USER: ", user)
    return user
