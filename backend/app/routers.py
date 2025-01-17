from fastapi import APIRouter

from app.users.router import router as user_router
from app.dependencies import DBSessionDep


router = APIRouter()

router.include_router(user_router, prefix="/user", tags=["user"])


@router.get("/status")
async def get_status(db_session: DBSessionDep):
    try:
        await db_session.connection()
        return {"db_connection": True}
    except:
        return {"db_connection": False}
