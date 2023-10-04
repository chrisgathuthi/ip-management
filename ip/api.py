import requests

response = requests.post("http://127.0.0.1:8000/api/token/",
                         json={"username": "timo", "password": "password"})
print(response.json())
print(response.status_code)
