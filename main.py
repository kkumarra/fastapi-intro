from fastapi import FastAPI, Request, Response
from google.cloud import firestore
#from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid4
import json
#from services.item_services import ItemService

app = FastAPI()
#item_service = ItemService()

#domain where this api is hosted for example : localhost:5000/docs to see documentation automagically generated.

db = firestore.Client(project='fastapi-intro')
tags_col = db.collection('tags')

@app.get("/")
def hello():
    return "Hello World"

@app.get("/health")
def health():
    return {"status": "Ok"}

@app.post("/increment")
async def increment_tag_value(request: Request):
    try:
        request_json = request.json()
        print(request_json)
        tag_doc = tags_col.document(request_json.id).get()
        if tag_doc:
            await tag_doc.set({ 'value': tag_doc.to_dict().get('value')+request_json.value })
    except Exception as e:
        return f"An Error Occured: {e}"

@app.get("/tag-stats")
def get_tag_stats():
    tag_docs = tags_col.stream()
    #docs_data = map(lambda x: x.to_dict(), tag_docs)
    docs_list = [doc.to_dict() for doc in tag_docs]
    print(docs_list)

    # for doc in tag_docs:
    #     print(f'{doc.id} => {doc.to_dict()}')
    return Response(json.dumps(docs_list), media_type="application/json")    


# @router.post("/items", response_model=Item, tags=["item"])
# def create_item(item_create: ItemCreate = Body(...,
#                                                example=ItemFactory.mock_item)):
#     """
#     create an item
#     """
#     return item_service.create_item(item_create)


# @router.get("/items/{id}", response_model=Item, tags=["item"])
# def get_item(id: str):
#     """
#     get any specific item
#     """
#     item = item_service.get_item(id)
#     if not item:
#         raise HTTPException(status_code=404, detail="Item not found.")
#     return item


# @router.get("/items", response_model=List[Item], tags=["item"])
# def list_items():
#     """
#     get many items
#     """
#     items = item_service.list_items()
#     if not items:
#         raise HTTPException(status_code=404, detail="Items not found.")
#     return items


# @app.post("/increment", response_model=Item, tags=["tags"])
# def increment_tag_value(item: Item):
#     """
#     update an item
#     """
#     item = item_service.get_item(name)
#     if not item:
#         #raise HTTPException(status_code=404, detail="Item not found.")
#         item_services.create_item(item)
#     return item_service.update_item(item)

