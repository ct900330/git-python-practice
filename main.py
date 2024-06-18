from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import shutil
import os
from typing import Optional
import requests


app = FastAPI()

UPLOAD_DIRECTORY = "uploads"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    file_location = f"{UPLOAD_DIRECTORY}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}
        
@app.get("/items/name/{name}")
async def read_item_name(name):
    return {"Hello" :name}

# 設全域變數儲存數字
items ={55: "Sample Item"}
 
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
        if item_id not in items:
            raise HTTPException(status_code=404, detail="Item not found")
        del items[item_id]
        return{"ok":True}
    


@app.get("/github")
async def get_gihub_api():
    response = requests.get("https://api.github.com")

    if response.status_code == 200:
        return {"Request was successful": response.json()}
    else:
        raise HTTPException(status_code=response.status_code, detail="Request failed")
    
# class Product(BaseModel):
#     name: str
#     price: float
#     description: Optional[str] = None
#     tax: Optional[float] = None   
     
# product = {
#     "foo": {"name": "Foo", "price": 50.2},
#     "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
# }
    
# @app.patch("/products/{product_id}", response_model=Product)
# async def update_product(product_id: str, product: Product):
#     if product_id not in products:
#         raise HTTPException(status_code=404, detail="Product not found")
#     stored_product_data = products[product_id]
#     stored_product_model = Product(**stored_product_data)
#     update_data = product.dict(exclude_unset=True)
#     updated_product = stored_product_model.copy(update=update_data)
#     products[product_id] = jsonable_encoder(updated_product)
#     return updated_product
        


