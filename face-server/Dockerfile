FROM python:3.7

WORKDIR /face-server

RUN apt-get update && apt-get install -y python3-opencv

RUN pip install cmake

RUN pip install dlib flask flask_cors imageio Pillow opencv-python

RUN pip install jsonpickle numba scikit-learn==0.22.2 filterpy pandas tensorflow==2.1.0

RUN pip install faiss-cpu

EXPOSE 5000

CMD ["python", "main.py"]
