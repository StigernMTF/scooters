from fastapi import FastAPI

from app.api.try_router import router as router_test
app = FastAPI()

app.include_router(router_test, prefix="/test", tags=["test"])