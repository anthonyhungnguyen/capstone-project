import os
import sys
import cv2
import dlib
import numpy as np
import subprocess
from datetime import datetime, timedelta
from time import time

# import ailibs libraries
from ailibs.utils import utils as UTILS
from registering.record_image import record_image as register_image
from ailibs.classifier.resnet.FaceClassifier import FaceClassifier
from ailibs.extractor.dlib.FaceExtractor import FaceExtractor
from ailibs.detector.dlib.FaceDetector import FaceDetector
from streaming.base_camera import BaseCamera
from streaming import PYTHON_PATH
from utils.ConfigurationStatus import CAMERA_CONFIG
from utils.ConfigurationStatus import update_db as DB_UPDATED_CHECKIN


LOG_TIME = True
CONFIG = CAMERA_CONFIG
CONFIG.update()

data_path = os.path.join(PYTHON_PATH, "ailibs_data")
shape_predictor_path = os.path.join(
    data_path, "extractor", "dlib", "shape_predictor_68_face_landmarks.dat")
face_recognition_path = os.path.join(
    data_path, "extractor", "dlib", "dlib_face_recognition_resnet_model_v1.dat")
classname_path = os.path.join(
    data_path, "classifier", "resnet", "classname.pickle")
model_path = os.path.join(data_path, "classifier", "resnet", "model.h5")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOT_FOUND_IMAGE = os.path.join(
    PYTHON_PATH, "ailibs_data", "testing", "images", "notfound.jpg")


FACE_DETECTOR = FaceDetector(log=LOG_TIME)
FACE_EXTRACTOR = FaceExtractor(
    shape_predictor=shape_predictor_path, face_recognition=face_recognition_path, log=LOG_TIME)
FACE_CLASSIFIER = FaceClassifier(
    classname=classname_path, model=model_path, log=LOG_TIME)

TRAINING_PROCESS = os.path.join(PYTHON_PATH, "trainning", "trainning.sh")

print('OPENCV_CAMERA_SOURCE', os.environ.get('OPENCV_CAMERA_SOURCE'))

UNKNOWN = "Unknown"
NONE = "none"


def draw_frame(frame, frame_count, star_time, name_list):
    """
    Draw frame
    Args:
        TBU
    Returns:
        TBU

    """

    name_pos = 30
    for key in name_list:
        name = key
        if name != UNKNOWN:
            frame = cv2.putText(frame, "Hello, {}".format(
                name), (10, name_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            name_pos += 30

    debug_pos = frame.shape[1] - 60
    frame = cv2.putText(frame, "DEBUG: FC: {}".format(
        str(frame_count)), (10, debug_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.putText(frame, str(star_time).split(" ")[
                1][:10], (150, debug_pos), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)
    current_time = datetime.now()
    cv2.putText(frame, str(current_time).split(" ")[
                1][:10], (300, debug_pos), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)
    return frame


class Camera(BaseCamera):
    video_source = 0

    def __init__(self):
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = CAMERA_CONFIG.CAMERA_URL

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(CAMERA_CONFIG.CAMERA_URL)
        if not camera.isOpened():
            print("CAMERA_CONFIG.CAMERA_URL", CAMERA_CONFIG.CAMERA_URL)
            frame = cv2.imread(NOT_FOUND_IMAGE)
            print("Could not start camera.'", frame.shape)
            yield cv2.imencode('.jpg', frame)[1].tobytes()
            # raise RuntimeError('Could not start camera.')
        SCALE = 1
        config_time = int(time())
        NAME_LIST = {}
        frame_count = 0
        skip_step = 1
        DURATION_TIME = 5
        SKIP_FRAME_STREAMING = 3
        SKIP_FRAME_DETECTING = 7
        SKIP_FRAME_RECOGNIZING = 28
        FACE_PADDING = 15
        FACE_RECOGNIZING = False

        # for MODE_FACE_REGISTERING
        MODE_FACE_REGISTERING = False  # load db
        FR_USER_ID = "nartin"
        FR_COUNT = 0
        FR_TOTAL = 5
        print("MODE_FACE_REGISTERING", MODE_FACE_REGISTERING, FR_USER_ID)

        # for MODE_FACE_TRAINING
        MODE_FACE_TRAINING = False  # load db
        FACE_CLASSIFIER_TRAINING = False  # load db

        star_time = datetime.now()
        latest_updated = int(time())
        while True:
            if int(time()) - config_time >= 1:
                config_time = int(time())
                CONFIG.update()
                if CAMERA_CONFIG.CAMERA_URL != Camera.video_source:
                    camera = cv2.VideoCapture(CAMERA_CONFIG.CAMERA_URL)
                    Camera.video_source = CAMERA_CONFIG.CAMERA_URL
                # camera = cv2.VideoCapture(CAMERA_CONFIG.CAMERA_URL)

            # read current frame
            success, frame = camera.read()

            if not success:
                print("END of video!!!!")
                frame_count = 0
                NAME_LIST = {}
                # star_time = datetime.now()
                camera = cv2.VideoCapture(CAMERA_CONFIG.CAMERA_URL)
                success, frame = camera.read()

            frame = frame[60:420, 0:640]
            frame_count += 1
            frame = cv2.resize(frame, (0, 0), fx=1/SCALE, fy=1/SCALE)
            # frame = UTILS.normalize_frame(frame)

            # streaming without processing
            if frame_count % skip_step != 0:
                if frame_count % SKIP_FRAME_STREAMING != 0:
                    continue
                frame = draw_frame(frame, frame_count, star_time, NAME_LIST)
                yield cv2.imencode('.jpg', frame)[1].tobytes()

            temp = cv2.resize(frame, (0, 0), fx=1/1, fy=1/1)

            # 1. MODE_FACE_REGISTERING
            # if MODE_FACE_REGISTERING:
            if CONFIG.USER_ID != NONE:
                FR_USER_ID = CONFIG.USER_ID
                skip_step = SKIP_FRAME_STREAMING
                if FR_COUNT >= FR_TOTAL:
                    CONFIG.deregister()
                    CONFIG.update()
                    MODE_FACE_REGISTERING = False
                    FR_COUNT = 0

                status, message = register_image(
                    frame, FACE_DETECTOR, FACE_EXTRACTOR, FR_USER_ID)
                if status:
                    FR_COUNT += 1
                else:
                    [fh, fw, channel] = frame.shape
                    frame = cv2.putText(
                        frame, message, (10, fh-30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

                print("MODE_FACE_REGISTERING", MODE_FACE_REGISTERING,
                      frame_count, FR_TOTAL, FR_COUNT)
                text = "Registering {}/{} images for [{}]".format(
                    FR_COUNT, FR_TOTAL, FR_USER_ID)
                frame = cv2.putText(
                    frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                yield cv2.imencode('.jpg', frame)[1].tobytes()
                continue

            # 2. MODE_FACE_TRAINING
            if MODE_FACE_TRAINING and not FACE_CLASSIFIER_TRAINING:
                subprocess.call("bash {}".format(TRAINING_PROCESS))
                # MODE_FACE_TRAINING = False
                FACE_CLASSIFIER_TRAINING = False

            # 3. MODE_FACE_STREAMING
            # update recoginzing status
            if frame_count % (SKIP_FRAME_RECOGNIZING) == 0:
                FACE_RECOGNIZING = True

            # detecting face features
            dets = FACE_DETECTOR.detect(temp)

            # extracting face features
            features_list = []
            face_list = []
            raw_image = frame.copy()
            for d in dets:
                latest_updated = int(time())
                [left, top, right, bottom] = FACE_DETECTOR.get_position(d)

                # cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 255))
                [t, l, r, b] = [max(0, top-int(2*FACE_PADDING)), max(0, left-FACE_PADDING), min(
                    right+FACE_PADDING, frame.shape[1]), min(bottom+FACE_PADDING, frame.shape[0])]
                cv2.rectangle(frame, (l, t), (r, b), (0, 255, 255))
                if FACE_RECOGNIZING:
                    features = FACE_EXTRACTOR.extract(temp, d)
                    features_list.append(features)
                    face = raw_image[t:b, l:r]
                    face_list.append(face)

            # classifying face
            if len(features_list) > 0:
                user_list = FACE_CLASSIFIER.classify_list(features_list)
                for i, user in enumerate(user_list):
                    if bool(user):
                        user['latest_time'] = int(time())
                        NAME_LIST[user['name']] = user
                        frame = cv2.putText(
                            frame, user['name'], (left, top), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)
                        checkin = {"employee_id": user['name'],
                                   "start_time": int(time()),
                                   "end_time": int(time())}
                        DB_UPDATED_CHECKIN(checkin, face_list[i])
                    FACE_RECOGNIZING = False
                    COUNTER = 0

            # update skipping frame for real-time streaming
            if len(dets) > 0:
                skip_step = SKIP_FRAME_DETECTING
            else:
                skip_step = SKIP_FRAME_STREAMING

            # clearing outdate user
            for key, value in list(NAME_LIST.items()):
                if int(time()) - NAME_LIST[key]["latest_time"] > DURATION_TIME:
                    print('Cleaning', int(
                        time()) - NAME_LIST[key]["latest_time"], 'frame_count', frame_count, len(dets))
                    del NAME_LIST[key]
                    FACE_RECOGNIZING = True
                else:
                    print('Frame_count', frame_count, len(
                        dets), str(int(time())), NAME_LIST)

            frame = draw_frame(frame, frame_count, star_time, NAME_LIST)
            yield cv2.imencode('.jpg', frame)[1].tobytes()
