from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api import renting_router
from app.models.db import init_db
from app.api.user_router import router as router_user
from app.api.renting_router import router as renting_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
app = FastAPI(lifespan=lifespan)

app.include_router(router_user, prefix="/user", tags=["user"])
app.include_router(renting_router, prefix="/rent", tags=["renting"])