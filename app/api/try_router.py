from app.service import try_service as ts
from fastapi import APIRouter
from app.schemas import first_pydantic_schema as fps

router = APIRouter()

@router.get("/hello")
def read_root():
    return ts.hello_world()


@router.get("/items/{item_id}")
def read_item(item_id: int, param: fps.Schema):
    return ts.read_item(param)