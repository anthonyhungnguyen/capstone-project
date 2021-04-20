import base64
import cv2
import numpy as np
import os
from time import time
from imutils import face_utils
from scipy.spatial import distance as dist


left_jaw = 0
mid_jaw = 8
right_jaw = 16
mid_nose = 34

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

    @staticmethod
    def is_frontal_face(image, det, face_extractor):
        """
        Check ratio of face.
        Args:
            TBU
        Return:
            TBU
        """
        shape = face_extractor.extract_shape(image, det)
        shape = face_utils.shape_to_np(shape)
        nose2leftjaw = dist.euclidean(shape[mid_nose], shape[left_jaw])
        nose2midjaw = dist.euclidean(shape[mid_nose], shape[mid_jaw])
        nose2rightjaw = dist.euclidean(shape[mid_nose], shape[right_jaw])

        if False:
            print("left_jaw", nose2leftjaw, 'mid_jaw', nose2midjaw, 'right_jaw', nose2rightjaw)
            cv2.line(image, (shape[mid_nose][0],shape[mid_nose][1]) , (shape[left_jaw][0],shape[left_jaw][1]), (0, 255, 0), thickness=1)
            cv2.line(image, (shape[mid_nose][0],shape[mid_nose][1]) , (shape[mid_jaw][0],shape[mid_jaw][1]), (0, 255, 0), thickness=1)
            cv2.line(image, (shape[mid_nose][0],shape[mid_nose][1]) , (shape[right_jaw][0],shape[right_jaw][1]), (0, 255, 0), thickness=1)

            frame = cv2.putText(image, str(int(nose2leftjaw)), (shape[left_jaw][0]+5, shape[left_jaw][1]), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)
            frame = cv2.putText(image, str(int(nose2midjaw)), (shape[mid_jaw][0], shape[mid_jaw][1]-15), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)
            frame = cv2.putText(image, str(int(nose2rightjaw)), (shape[right_jaw][0]-30, shape[right_jaw][1]), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)

        minlf = min(nose2leftjaw, nose2rightjaw)
        if abs(nose2leftjaw - nose2rightjaw) < 1/2*minlf:
            if abs(minlf - nose2midjaw) < 1/2*min(minlf, nose2rightjaw):
                return True
            else:
                return False
        else:
            return False
