import requests
import cv2
import json
import numpy as np
import base64
import json


class CropAndAugment:
    def __init__(self, server_url):
        self.server_url = server_url
        self.crop_url = self.server_url + "/face/crop"
        self.augment_url = self.server_url + "/face/augment"
        self.headers = {
            "content-type": "image/jpeg"
        }

    def crop(self, image_path):
        img = cv2.imread(image_path)
        _, img_encoded = cv2.imencode('.jpg', img)

        response = requests.post(
            self.crop_url, data=img_encoded.tostring(), headers=self.headers)
        img = base64.b64decode(response.text)
        with open('./crop.jpg', 'wb') as f:
            f.write(img)

    def augment(self, image_path):
        img = cv2.imread(image_path)
        _, img_encoded = cv2.imencode('.jpg', img)

        response = requests.post(
            self.augment_url, data=img_encoded.tostring(), headers=self.headers)
        augment_array = json.loads(response.text)['augment_array']
        for index, augment_img in enumerate(augment_array):
            img = base64.b64decode(augment_img)
            with open(f'./augment_{index}.jpg', 'wb') as f:
                f.write(img)
