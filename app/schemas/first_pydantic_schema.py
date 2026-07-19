from pydantic import BaseModel

class Schema(BaseModel):
    item_id: int
    title: str