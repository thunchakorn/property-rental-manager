from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.dependencies import DBSessionDep

from app.routers import router
from app.config import settings


app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router, prefix=settings.API_V1_PREFIX)
