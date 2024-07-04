from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from .services import get_user_by_id
from .models import User

from ..config import settings
from ..security import read_access_token
from ..dependencies import DBSessionDep

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/user/access-token"
)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db_session: DBSessionDep
) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = read_access_token(token)
        user_id: int = payload.get("sub")
        if not user_id:
            raise InvalidTokenError
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user_by_id(user_id=user_id, db_session=db_session)
    if not user:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
