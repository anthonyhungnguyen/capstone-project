import base64
import cv2
import numpy as np


class FaceUtilities():

    def __init__(self, **kwargs):
        super().__init__()
        self.log = kwargs.get('log', False)

    @staticmethod
    def img_to_base64(img):
        _, buffer = cv2.imencode('.jpg', img)
        return base64.b64encode(buffer).decode('utf-8')

    @staticmethod
    def numpy_to_img(data):
        nparr = np.fromstring(data, np.uint8)
        img = cv2.imdecode(nparr, cv2.COLOR_RGB2BGR)
        return np.array(img, dtype=np.uint8)

    @staticmethod
    def flip_face(img, flip_code):
        return cv2.flip(img, flip_code)

    @staticmethod
    def increase_brightness(img, value):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value

        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return img
