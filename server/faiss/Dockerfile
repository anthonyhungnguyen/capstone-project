FROM bitnami/python:3.6

USER root

WORKDIR /app

RUN pip install --upgrade pip && pip install --no-cache-dir tensorflow==2.5.0

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY . ./

RUN pip install --no-cache-dir cmake

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python", "run/server_python.py" ]

