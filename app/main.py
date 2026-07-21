from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.models.db import init_db
from app.api.user_router import router as router_test

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
app = FastAPI(lifespan=lifespan)

app.include_router(router_test, prefix="/test", tags=["test"])