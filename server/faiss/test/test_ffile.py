from fastapi import FastAPI, UploadFile, File
import json


app = FastAPI()


@app.post("/file/")
async def create_upload_file(file: UploadFile = File(...)):

    # return {"filename": json.loads(file.file.read())}
    # print(json.loads(file.file.read()))
    return {"filename": file.file.read()}
