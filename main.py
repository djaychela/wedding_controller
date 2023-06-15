from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float

app = FastAPI()

@app.get("/")
async def root():
    return {"message" : "Hello World!"}

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict
    print(item_dict)
    return item
