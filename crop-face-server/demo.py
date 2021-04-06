
import dlib
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from imageio import imread
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
    def convertBase64ToNumpyArray(request):
        jsonData = request.data
        photo = json.loads(jsonData)['data']
        imgstr = re.search(r'base64,(.*)', photo).group(1)
        image_bytes = io.BytesIO(base64.b64decode(imgstr))
        im = Image.open(image_bytes)
        return np.array(im, dtype=np.uint8)

    def convertNumpyToBase64(img):
        pil_img = Image.fromarray(img)
        buff = io.BytesIO()
        pil_img.save(buff, format="JPEG")
        new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")
        return new_image_string
    frame = convertBase64ToNumpyArray(request)
    dets = detector(frame)
    for d in dets:
        shape = predictor(frame, d)
        face_frame = dlib.get_face_chip(frame, shape, size=INPUT_SIZE)
        base64Img = convertNumpyToBase64(face_frame)
        return f"data:image/jpeg;base64,{base64Img}"
    return None

@app.route("/face/augment", methods=["POST"])
@cross_origin()
def augment_face():
    def convertNumpyToBase64(img):
        pil_img = Image.fromarray(img)
        buff = io.BytesIO()
        pil_img.save(buff, format="JPEG")
        new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")
        return new_image_string

    def flipFace(image):
        return cv2.flip(image, 1)
    def increaseBrightness(img, value):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value

        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return img
    data = request.data
    imageString = json.loads(data.decode('utf-8'))['faceImage']
    image = img = imread(io.BytesIO(base64.b64decode(imageString)))

    origin30Image = increaseBrightness(image, 30)
    flipImage = flipFace(image)
    flip30Image = increaseBrightness(flipImage, 30)
    flip50Image = increaseBrightness(flipImage, 50)
    return json.dumps({
        "augmentFaceArray": [convertNumpyToBase64(origin30Image), convertNumpyToBase64(flipImage), convertNumpyToBase64(flip30Image), convertNumpyToBase64(flip50Image)]
    })



app.run(host='0.0.0.0', port='5000', debug=True)
