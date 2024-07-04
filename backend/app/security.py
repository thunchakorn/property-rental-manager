import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(payload: dict) -> str:
    payload = payload.copy()
    payload.update(
        {
            "exp": (
                datetime.now()
                + timedelta(minutes=settings.JWT_ACCESS_EXPIRE_IN_MINUTES)
            )
        }
    )

    token = jwt.encode(
        payload=payload, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )

    return token


def read_access_token(token: str):
    payload = jwt.decode(
        token, key=settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
    )
    return payload