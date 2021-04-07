FROM capstone-project_crop-face-server:latest

WORKDIR /faiss-server

RUN apt-get update && apt-get install -y python3-opencv

RUN pip install faiss-cpu pickle-mixin confluent-kafka pandas tensorflow


CMD ["python", "run/server-python.py"]