from __init__ import PYTHON_PATH
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from imageio import imread
import json
from PIL import Image
import base64
import io
import re
import cv2
from utils import AIlibs

app = Flask(__name__)
ailibs_instance = AIlibs.AILIBS()
face_extractor_instance = ailibs_instance.EXTRACTOR
face_detector_instance = ailibs_instance.DETECTOR
numpy_to_img = ailibs_instance.UTILITIES.numpy_to_img
img_to_base64 = ailibs_instance.UTILITIES.img_to_base64
flip_face = ailibs_instance.UTILITIES.flip_face
increase_brightness = ailibs_instance.UTILITIES.increase_brightness
detector = face_detector_instance.detect
extract_shape = face_extractor_instance.extract_shape
get_face_chip = face_extractor_instance.get_face_chip
extract_feature = face_extractor_instance.extract_without_det
INPUT_SIZE = 160


@app.route("/face/crop", methods=["POST"])
@cross_origin()
def crop_face():
    frame = numpy_to_img(request.data)
    dets = detector(frame)
    for d in dets:
        shape = extract_shape(frame, d)
        face_frame = get_face_chip(
            frame, shape, size=INPUT_SIZE)
        return img_to_base64(face_frame)
    return "hello"


@app.route("/face/augment", methods=["POST"])
@cross_origin()
def augment_face():
    image = numpy_to_img(request.data)

    origin_30 = increase_brightness(
        image, 30)
    flip = flip_face(image, 1)
    flip_30 = increase_brightness(
        flip, 30)
    flip_50 = increase_brightness(
        flip, 50)
    return {
        "augment_array": [img_to_base64(origin_30), img_to_base64(flip), img_to_base64(flip_30), img_to_base64(flip_50)]
    }


@app.route('/face/feature', methods=["POST"])
def feature_face():
    image = numpy_to_img(request.data)
    return {
        'feature': extract_feature(image).tolist()
    }


app.run(host='0.0.0.0', port='5000', debug=True)
