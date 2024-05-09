from fastapi import FastAPI,Query
from enum import Enum
import uvicorn
from typing import Union
from pydantic import BaseModel

app = FastAPI()

#첫걸음
@app.get("/first-steps/")
async def root():
    return {"message : " : "Hello, World"}

#경로 매개변수
@app.get("/path-params/ReadInt/{item_id}")
async def read_item(item_id : int):
    return {"item_id": item_id}

@app.get("/path-params/ReadItem/{input}")
async def read_input(input):
    return {"input : ": input}

@app.get("/path-params/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/path-params/ReadUserID/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/path-params/ReadClass/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}

@app.get("/path-params/ReadFilePath/{file_path:path}")
async def read_file(file_path : str):
    return {"file_path" : file_path}

#쿼리 매개변수
fake_items_db = [{"item_name" : "Foo"}, {"items_name" : "Bar"}, {"item_name": "Baz"}]
@app.get("/query-params/QueryParameters/")
async def read_item(skip: int = 0, limit : int = 10):
    return fake_items_db[skip : skip + limit]

@app.get("/query-params/OptinalParameters/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

@app.get("/query-params/QueryConversion/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

@app.get("/query-params/RequireProperty/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item

@app.get("/query-params/MultipleRequireProperty/{item_id}")
async def read_user_item(
    item_id: str, needy: str, skip: int = 0, limit: Union[int, None] = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item

#요청 본문
class Item(BaseModel):
    name        : str
    description : str   | None = None
    price       : float
    tax         : float | None = None

@app.post("/body/ItemPrint/")
async def create_item(item: Item):
    return item

@app.post("/body/PricePlusTax/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@app.put("/body/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

#쿼리 매개변수와 문자열 검증
@app.get("/query-params-str-validations/ParameterVerification/")
async def read_items(q: Union[str, None] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.get("/query-params-str-validations/AdditionalVerification/")
async def read_items(q: Union[str, None] = Query(default=None, max_length=5)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

#'쿼리 매개변수와 문자열 검증 - 기본값으로 Query 사용'부터 해야함

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0",port=8008)