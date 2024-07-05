from typing import Annotated
from jwt.exceptions import DecodeError, ExpiredSignatureError

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from . import services
from . import schemas
from .dependencies import CurrentUserDep

from ..dependencies import DBSessionDep
from .. import security

router = APIRouter()


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserPublic,
    summary="Create new user without the need to be logged in",
)
async def register_user(user_create: schemas.UserCreate, db_session: DBSessionDep):
    """
    Create new user without the need to be logged in.

    **password**: must be longer than 4 characters.
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

    access_token = security.create_access_token(payload={"sub": user.id})
    refresh_token = security.create_refresh_token(payload={"sub": user.id})

    return schemas.Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh-access-token", response_model=schemas.Token)
async def refresh_access_token(
    refresh_data: schemas.RefreshRequest, db_session: DBSessionDep
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = security.read_access_token(refresh_data.refresh_token)
        user_id: int = payload.get("sub")
        if not user_id:
            raise credentials_exception
    except DecodeError:
        raise credentials_exception
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await services.get_user_by_id(user_id=user_id, db_session=db_session)
    if not user:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    access_token = security.create_access_token(payload={"sub": user.id})
    refresh_token = security.create_refresh_token(payload={"sub": user.id})

    return schemas.Token(access_token=access_token, refresh_token=refresh_token)


@router.get("/me", response_model=schemas.UserPublic)
async def get_me(current_user: CurrentUserDep):
    return current_user
