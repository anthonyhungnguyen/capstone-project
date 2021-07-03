import requests
import base64

url = 'http://127.0.0.1:8000/face'

with open("vector.index", "rb") as file:
    faiss_encode = base64.b64encode(file.read())

faiss_data = {"faiss": "phuc"}
x = requests.post(url, data=faiss_data)

print(x)
