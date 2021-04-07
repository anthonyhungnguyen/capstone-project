FROM python:3.7

WORKDIR /faiss-server

RUN apt-get update && apt-get install -y python3-opencv libomp-dev

RUN pip install opencv-python numpy faiss pickle-mixin numpy

EXPOSE 6000

CMD ["python", "run/server_python.py"]