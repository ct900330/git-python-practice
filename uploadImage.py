from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import shutil
import os

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

@app.get("/")
async def main():
    content = """
    <body>
    <form action="/uploadfile/" enctype="multipart/form-data" method="post">
    <input name="file" type="file">
    <input type="submit">
    </form>
    </body>
    """
    return HTMLResponse(content=content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
