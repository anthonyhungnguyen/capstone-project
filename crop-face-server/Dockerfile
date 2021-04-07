FROM python:3.7

WORKDIR /crop-face-server

RUN apt-get update && apt-get install -y python3-opencv

RUN pip install cmake

RUN pip install dlib flask flask_cors imageio Pillow opencv-python

EXPOSE 5000

CMD ["python", "demo.py"]