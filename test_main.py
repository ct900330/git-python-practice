from fastapi.testclient import TestClient
from main import app
import os

client = TestClient(app)

def test_upload_file():
    response = client.post("/uploadfile/", files={"file": ("test.txt", b"this is a test")})
    assert response.status_code == 200
    expected_message = "file 'test.txt' saved at 'uploads/test.txt'"
    actual_message = response.json()["info"].replace("\\", "/")
    assert actual_message == expected_message

def test_read_image():
    response = client.get("/images/test.txt")
    assert response.status_code == 200
    assert response.content == b"this is a test"

def test_delete_image():
    response = client.delete("/images/test.txt")
    assert response.status_code == 200
    assert response.json() == {"info": "Image 'test.txt' deleted"}

def test_update_image_name():
    # Upload a file for renaming test
    client.post("/uploadfile/", files={"file": ("old_name.txt", b"this is a test")})
    response = client.put("/images/old_name.txt", data={"new_name": "new_name.txt"})
    assert response.status_code == 200
    assert response.json() == {"info": "Image 'old_name.txt' renamed to 'new_name.txt'"}
    # Clean up
    client.delete("/images/new_name.txt")
