# from fastapi import FastAPI
# from typing import Dict, Any

# app = FastAPI()


# @app.post("/face/")
# async def create_item(item: Dict[Any, Any]):
#     print("TEST:", item)
#     return item

# import json
# from typing import List
# from fastapi import FastAPI, Query, Depends


# app = FastAPI(debug=True)


# def location_dict(locations: List[str] = Query(...)):
#     return list(map(json.loads, locations))


# @app.get("/face")
# def operation(locations: list = Depends(location_dict)):
#     return locations

# from typing import Optional
# from fastapi import FastAPI

# from pydantic import BaseModel


# class Package(BaseModel):
#     name: str
#     number: str
#     description: Optional[str] = None


# app = FastAPI()


# @app.get('/')
# async def hello_world():
#     return {'Hello': 'World'}


# @app.post("/package/{priority}")
# async def make_package(priority: int, package: Package, value: bool):
#     return {"priority": priority, **package.dict(), "value": value}


from typing import Optional
from fastapi import FastAPI

from pydantic import BaseModel


class Package(BaseModel):
    faiss: str


app = FastAPI()


@app.get('/')
async def hello_world():
    return {'Hello': 'World'}


@app.post("/face")
async def raspberry(package: Package):
    return {**package.dict()}
