import requests

response = requests.get("https://api.github.com")

if response.status_code == 200:
    print("Request was successful")
    print(response.json())
else:
    print(f"Request failed: {response.status_code}")
