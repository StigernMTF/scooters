from app.schemas import first_pydantic_schema

def read_item(param: first_pydantic_schema.Schema):
    return {"item_id": param.item_id}

def hello_world():
    return "Hello world"