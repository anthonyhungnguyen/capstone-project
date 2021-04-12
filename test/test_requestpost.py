import requests
import base64

url = 'http://192.168.1.6:8000'

with open("vector.index", "rb") as file:
    faiss_encode = base64.b64encode(file.read())

faiss_data = {'faiss': "phuc"}
x = requests.post(url, data=faiss_data)

print(x)
