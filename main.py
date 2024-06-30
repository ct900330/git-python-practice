from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import os

app = FastAPI()

UPLOAD_DIRECTORY = "uploads"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_location, "wb") as buffer:
        buffer.write(file.file.read())
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}

@app.get("/images/{image_name}", response_class=FileResponse)
async def read_image(image_name: str):
    file_location = os.path.join(UPLOAD_DIRECTORY, image_name)
    if not os.path.exists(file_location):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(file_location)

@app.delete("/images/{image_name}")
async def delete_image(image_name: str):
    file_location = os.path.join(UPLOAD_DIRECTORY, image_name)
    if not os.path.exists(file_location):
        raise HTTPException(status_code=404, detail="Image not found")
    os.remove(file_location)
    return {"info": f"Image '{image_name}' deleted"}

@app.put("/images/{image_name}")
async def update_image_name(image_name: str, new_name: str):
    file_location = os.path.join(UPLOAD_DIRECTORY, image_name)
    new_file_location = os.path.join(UPLOAD_DIRECTORY, new_name)
    if not os.path.exists(file_location):
        raise HTTPException(status_code=404, detail="Image not found")
    if os.path.exists(new_file_location):
        raise HTTPException(status_code=400, detail="New image name already exists")
    os.rename(file_location, new_file_location)
    return {"info": f"Image '{image_name}' renamed to '{new_name}'"}
