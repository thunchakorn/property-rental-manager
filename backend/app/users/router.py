from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from . import services
from . import schemas
from .dependencies import CurrentUserDep
from .models import User

from ..dependencies import DBSessionDep
from ..security import create_access_token

router = APIRouter()


@router.post(
    "/signup", status_code=status.HTTP_201_CREATED, response_model=schemas.UserPublic
)
async def register_user(user_create: schemas.UserCreate, db_session: DBSessionDep):
    """
    Create new user without the need to be logged in.
    """
    user = await services.get_user_by_email(
        email=user_create.email, db_session=db_session
    )
    if user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user with this email already exists in the system",
        )

    user = await services.create_user(user_create=user_create, db_session=db_session)
    await db_session.commit()
    await db_session.refresh(user)

    return user


@router.post("/access-token", response_model=schemas.Token)
async def get_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db_session: DBSessionDep
):
    user = await services.autheticate_user(
        email=form_data.username, password=form_data.password, db_session=db_session
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    access_token = create_access_token(payload={"sub": user.id})

    return schemas.Token(access_token=access_token)


@router.get("/me", response_model=schemas.UserPublic)
async def get_me(current_user: CurrentUserDep):
    return current_user
