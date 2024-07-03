from fastapi import FastAPI
from sqlalchemy import select

from models import User
from db import DBSessionDep

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/status")
async def get_status(db_session: DBSessionDep):
    return {"status": bool(db_session)}


@app.get("/users")
async def get_users(db_session: DBSessionDep):
    stmt = select(User)
    results = await db_session.scalars(stmt)
    users = results.all()
    return {"users": users}
