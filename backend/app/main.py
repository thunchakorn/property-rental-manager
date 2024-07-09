from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import router
from app.config import settings
from app.db import LocalSession
from app.security import get_password_hash

from app.users.models import User


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_session = LocalSession()

    user = await db_session.get(User, 0)
    if user:
        await db_session.delete(user)
        await db_session.commit()

    root_user = User(
        id=0,
        email=settings.ROOT_EMAIL,
        password=get_password_hash(password=settings.ROOT_PASSWORD),
        first_name="root",
        last_name="root",
    )
    db_session.add(root_user)
    await db_session.commit()
    yield

    await db_session.delete(root_user)
    await db_session.commit()


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan, version="0.0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router, prefix=settings.API_V1_PREFIX)
