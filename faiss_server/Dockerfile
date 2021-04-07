FROM capstone-project_crop-face-server:latest

WORKDIR /faiss-server

RUN apt-get update && apt-get install -y libomp-dev

RUN pip install faiss-cpu pickle-mixin confluent-kafka pandas tensorflow


CMD ["python", "run/server_python.py"]
