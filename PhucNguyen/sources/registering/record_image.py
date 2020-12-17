import os
import django
from time import time
import cv2

FACE_REGISTERING_COUNT = 0
FACE_REGISTERING_TOTAL = 100

from __init__ import PYTHON_PATH
from ailibs.utils import utils as UTILS
os.environ['DJANGO_SETTINGS_MODULE'] = 'checkin.settings'
django.setup()
from checkin.facecheckin.models import Employee, FaceImage, CheckInTime, Configuration, PretrainedImage
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DATABASE_PATH = os.path.join(os.path.dirname(PYTHON_PATH), "storage", "dbfaces")
IMAGE_PADDING = 10


class FACE_MESSAGE:
    NOT_DEFINE = "NONE"
    SUCCESS = "The face image is successful recording."
    ERR_NO_FACE = "NO FACE is detected !!!"
    ERR_MUTIL_FACES = "Too MANY FACES  are detected !!!"
    ERR_NON_FRONTAL_FACE = "Please show YOUR FRONTAL FACE !!!"
    ERR_EXCEPTION = "EXCEPTION"

def record_image(frame, face_detector, face_extractor, user_id, draw_face=True):

    status = False
    message = FACE_MESSAGE.NOT_DEFINE
    try:
        
        user_path = os.path.join(DATABASE_PATH, user_id)
        if not os.path.isdir(user_path):
            os.mkdir(user_path)

        dets = face_detector.detect(frame)

        # check if no face is detected
        if len(dets) == 0:
            message = FACE_MESSAGE.ERR_NO_FACE
            return status, message
        # check if mutil faces are detected
        if len(dets) > 1:
            message = FACE_MESSAGE.ERR_MUTIL_FACES
            return status, message
        # check if show frontal face
        if not UTILS.is_frontal_face(frame, dets[0], face_extractor):
            message = FACE_MESSAGE.ERR_NON_FRONTAL_FACE
            return status, message
        # check if non-blurring face

        # check if low-brightness face

        # save face image
        start = int(time())
        left = dets[0].left()
        top = dets[0].top()
        right = dets[0].right()
        bottom = dets[0].bottom()
        p = IMAGE_PADDING
        face = frame[max(0,top-p):min(bottom+p, frame.shape[0]), max(0,left-p):min(right+p, frame.shape[1])]

        # save face image for user
        pretrain = PretrainedImage(employee_id=user_id)
        pretrain.save()
        image_name = os.path.join(user_path, str(pretrain.id)+'.jpg')
        cv2.imwrite(image_name, face)

        # draw face
        if draw_face:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 255))

        message = FACE_MESSAGE.SUCCESS
        status = True
        return status, message
    except Exception as e:
        print("Exception", e)
        message = FACE_MESSAGE.ERR_EXCEPTION  + str(e)
        return status, message