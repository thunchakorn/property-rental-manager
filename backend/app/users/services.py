from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession


from .models import User
from . import schemas
from .. import security


async def get_user_by_email(email: str, db_session: AsyncSession) -> User:
    stmt = select(User).filter_by(email=email)
    user = await db_session.execute(stmt)
    return user.scalar_one_or_none()


async def get_user_by_id(user_id: int, db_session: AsyncSession) -> User:
    stmt = select(User).filter_by(id=user_id)
    user = await db_session.execute(stmt)
    return user.scalar_one_or_none()


async def create_user(
    user_create: schemas.UserCreate, db_session: AsyncSession
) -> User:
    user = User(
        **user_create.model_dump(exclude={"password"}),
        password=security.get_password_hash(password=user_create.password),
    )
    db_session.add(user)

    return user


async def autheticate_user(email: str, password: str, db_session: AsyncSession) -> User:
    user = await get_user_by_email(email=email, db_session=db_session)
    if not user:
        return None
    if not security.verify_password(password, user.password):
        return None

    return user
