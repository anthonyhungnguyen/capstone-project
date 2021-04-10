
import dlib
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from imageio import imread
import jsonpickle
import json
from PIL import Image
import base64
import io
import re
import cv2

app = Flask(__name__)
CORS(app)

detector = dlib.get_frontal_face_detector()

predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
INPUT_SIZE = 160

min_dist = float('inf')


@app.route("/face/crop", methods=["POST"])
@cross_origin()
def crop_face():
    nparr = np.fromstring(request.data, np.uint8)
    img = cv2.imdecode(nparr, cv2.COLOR_RGB2BGR)
    frame = np.array(img, dtype=np.uint8)
    dets = detector(frame)
    for d in dets:
        shape = predictor(frame, d)
        face_frame = dlib.get_face_chip(frame, shape, size=INPUT_SIZE)
        _, buffer = cv2.imencode('.jpg', face_frame)
        img_str = base64.b64encode(buffer)
        return img_str
    return "hello"


@app.route("/face/augment", methods=["POST"])
@cross_origin()
def augment_face():
    def to_base64(img):
        _, buffer = cv2.imencode('.jpg', img)
        img_str = base64.b64encode(buffer)
        return img_str

    def flip_face(image):
        return cv2.flip(image, 1)

    def increase_brightness(img, value):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value

        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return img
    nparr = np.fromstring(request.data, np.uint8)
    image = cv2.imdecode(nparr, cv2.COLOR_RGB2BGR)

    origin30Image = increase_brightness(image, 30)
    flipImage = flip_face(image)
    flip30Image = increase_brightness(flipImage, 30)
    flip50Image = increase_brightness(flipImage, 50)
    return {
        "augment_array": [to_base64(origin30Image), to_base64(flipImage), to_base64(flip30Image), to_base64(flip50Image)]
    }


app.run(host='0.0.0.0', port='5000', debug=True)
