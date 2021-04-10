import requests
import cv2
import json
import numpy as np
import base64


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

        response = requests.post(
            self.crop_url, data=img.tostring(), headers=self.headers)
        img = base64.b64decode(response.text)
        with open('./crop.jpg', 'wb') as f:
            f.write(img)
