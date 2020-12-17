import os
import sys
import cv2
import dlib
import uuid
import numpy as np
import subprocess
from datetime import datetime, timedelta
from time import time, localtime, strftime

# import ailibs libraries
from ailibs.utils import utils as UTILS
from registering.record_image import record_image as register_image
from streaming.base_camera import BaseCamera
from streaming import PYTHON_PATH
from utils.AIlibs import AILIBS
from utils.Status import TRAINING_STATUS
from utils.ConfigurationStatus import CAMERA_CONFIG
from utils.ConfigurationStatus import update_db as DB_UPDATED_CHECKIN
from utils.mail_alert.MailAlert import MailAlert


# LOG_TIME = True
mCONFIG = CAMERA_CONFIG
mCONFIG.update()

mAILIBS = AILIBS
AILIBS.update(mCONFIG.TRAINING_STATUS)
# time.sleep(5)
if AILIBS.load_model():
    mCONFIG.LOGGER.info("Succeeded loading AILIBS models.")
else:
    mCONFIG.LOGGER.error("Failed loading AILIBS models.")

utils_path = os.path.join(PYTHON_PATH, "utils")
mail_receiver_path = os.path.join(
    utils_path, "mail_alert", "receiver_address.txt")
alert_image_path = os.path.join(utils_path, "mail_alert", "images")

MAIL_ALERT = MailAlert(mail_receiver=mail_receiver_path,
                        images=alert_image_path)
NOT_FOUND_IMAGE = os.path.join(PYTHON_PATH, "ailibs_data", "testing", "images", "notfound.jpg")
UNKNOWN = "Unknown"
NONE = "none"
NOONE = {}


def draw_frame(frame, frame_count, star_time, name_list, line_track, face_trackers):
    """
    Draw frame
    Args:
        TBU
    Returns:
        TBU

    """
    red_color = (0,0,255)
    green_color = (0,255,0)

    name_pos = 50
    for key in name_list:
        name = name_list[key]['name']
        if name != UNKNOWN:
            if name != "Unknown ALERT":
                # frame = cv2.putText(frame, "Wellcome {} to HaNoi Room !".format(
                frame = cv2.putText(frame, "Welcome {} to Three O'clock Coffee !".format(
                name.replace("ACCEPT", "")), (50, name_pos), cv2.FONT_HERSHEY_SIMPLEX, 1.3, green_color, 3)
            # frame = cv2.putText(frame, "Warning: {} {} {}".format(
            #     name, int(name_list[key]['score']), strftime('%H:%M:%S', localtime(name_list[key]['latest_time']))), (10, name_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                name_pos += 50
            else:
                frame = cv2.putText(frame, "Warning: {}".format(
                name ), (50, name_pos), cv2.FONT_HERSHEY_SIMPLEX, 1.3, red_color, 3)
            # frame = cv2.putText(frame, "Hello, {} {} {}".format(
            #     name, int(name_list[key]['score']), strftime('%H:%M:%S', localtime(name_list[key]['latest_time']))), (10, name_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                name_pos += 50
        else:
            pass
            # frame = cv2.putText(frame, "Warning: {}".format(
            #     name ), (200, name_pos), cv2.FONT_HERSHEY_SIMPLEX, 1.5, red_color, 3)
            # # frame = cv2.putText(frame, "Warning: {} {} {}".format(
            # #     name, int(name_list[key]['score']), strftime('%H:%M:%S', localtime(name_list[key]['latest_time']))), (10, name_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            # name_pos += 50

    if False:
        for (faceID, centroid) in face_trackers.items():
            if faceID in line_track.keys():
                start_point = tuple()
                end_point = tuple()
                centroid_trackors = line_track[faceID]
                for i, c in enumerate(centroid_trackors):
                    # cv2.circle(frame, (c[0], c[1]), 4, (0, 255, 0), -1)
                    if i == 0:
                        end_point = (c[0], c[1])
                    else:
                        start_point = end_point
                        end_point = (c[0], c[1])
                        cv2.line(frame, start_point, end_point, (255, 150, 0), 1)

    # debug_pos = frame.shape[1] - 60
    # frame = cv2.putText(frame, "DEBUG: FC: {}".format(
    #     str(frame_count)), (10, debug_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # cv2.putText(frame, str(star_time).split(" ")[
    #             1][:10], (150, debug_pos), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)
    # current_time = datetime.now()
    # cv2.putText(frame, str(current_time).split(" ")[
    #             1][:10], (300, debug_pos), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)
    return frame


class Camera(BaseCamera):
    video_source = 0
    TRAINING_STATUS = mCONFIG.TRAINING_STATUS

    def __init__(self):
        super(Camera, self).__init__()

    @ staticmethod
    def set_video_source(source):
        Camera.video_source = mCONFIG.CAMERA_URL

    @ staticmethod
    def frames():
        camera = cv2.VideoCapture(mCONFIG.CAMERA_URL)
        if not camera.isOpened():
            print("mCONFIG.CAMERA_URL", mCONFIG.CAMERA_URL)
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
        SKIP_FRAME_STREAMING = 1
        SKIP_FRAME_DETECTING = 1
        SKIP_FRAME_RECOGNIZING = 1
        SKIP_FRAME_TRACKING = 1
        FACE_PADDING = 15
        FACE_RECOGNIZING = False
        FACE_TRACKING = False
        CURRENT_TRAINING_STATUS = mCONFIG.TRAINING_STATUS

        # for MODE_FACE_REGISTERING
        MODE_FACE_REGISTERING = False  # load db
        FR_USER_ID = "PhucNguyen"
        FR_COUNT = 0
        print("MODE_FACE_REGISTERING", MODE_FACE_REGISTERING, FR_USER_ID)

        # for MODE_FACE_TRAINING
        MODE_FACE_TRAINING = False  # load db
        FACE_CLASSIFIER_TRAINING = False  # load db

        # for TRACKING:
        ID = {}
        trackcount = {}
        line_track = {}

        star_time = datetime.now()
        latest_updated = int(time())
        while True:
            if int(time()) - config_time >= 1:
                config_time = int(time())
                mCONFIG.update()
                if mCONFIG.CAMERA_URL != Camera.video_source:
                    mCONFIG.LOGGER.info(" UPDATING CAMERA_URL {} to {}".format(Camera.video_source, mCONFIG.CAMERA_URL))
                    camera = cv2.VideoCapture(mCONFIG.CAMERA_URL)
                    Camera.video_source = mCONFIG.CAMERA_URL

                if mCONFIG.TRAINING_STATUS != Camera.TRAINING_STATUS:
                    mAILIBS.update(Camera.TRAINING_STATUS)
                    mCONFIG.LOGGER.info(" UPDATING TRAINING_STATUS {} to {}".format(Camera.TRAINING_STATUS, mCONFIG.TRAINING_STATUS))
                    Camera.TRAINING_STATUS = mCONFIG.TRAINING_STATUS
                # camera = cv2.VideoCapture(mCONFIG.CAMERA_URL)

            # read current frame
            success, frame = camera.read()

            if not success:
                # star_time = datetime.now()
                camera = cv2.VideoCapture(mCONFIG.CAMERA_URL)
                success, frame = camera.read()
                print("________", mCONFIG.CAMERA_URL, type(mCONFIG.CAMERA_URL))
                continue

            # frame = frame[60:420, 0:640]
            frame_count += 1

            print("FRAME COUNT: ", frame_count)
            frame = cv2.resize(frame, (0, 0), fx=1/SCALE, fy=1/SCALE)
            # frame = UTILS.normalize_frame(frame)

            # 1. MODE_FACE_TRAINING
            if mCONFIG.TRAINING_STATUS == TRAINING_STATUS.IN_PROCESSING:
                # mCONFIG.LOGGER.info("TRAINING_STATUS.IN_PROCESSING")
                text = "Training Face Recognition Model"
                frame = cv2.putText(
                    frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2) 
                print("FC {} training...".format(frame_count))
                yield cv2.imencode('.jpg', frame)[1].tobytes()
                continue

            # streaming without processing
            if frame_count % skip_step != 0:
                if frame_count % SKIP_FRAME_STREAMING != 0:
                    continue
                frame = draw_frame(frame, frame_count,
                                   star_time, NAME_LIST, line_track, face_trackers)
                yield cv2.imencode('.jpg', frame)[1].tobytes()

            temp = cv2.resize(frame, (0, 0), fx=1/1, fy=1/1)

            # 2. MODE_FACE_REGISTERING
            if mCONFIG.USER_ID != NONE:
                FR_USER_ID = mCONFIG.USER_ID
                skip_step = SKIP_FRAME_STREAMING
                if FR_COUNT >= mCONFIG.FR_TOTAL:
                    mCONFIG.deregister()
                    mCONFIG.update()
                    MODE_FACE_REGISTERING = False
                    FR_COUNT = 0
                print("FACE_DETECTOR", type(mAILIBS.DETECTOR))
                status, message = register_image(
                    frame, mAILIBS.DETECTOR, mAILIBS.EXTRACTOR, FR_USER_ID)
                if status:
                    FR_COUNT += 1
                else:
                    [fh, fw, channel] = frame.shape
                    frame = cv2.putText(
                        frame, message, (10, fh-30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

                # print("MODE_FACE_REGISTERING", MODE_FACE_REGISTERING,
                #       frame_count, mCONFIG.FR_TOTAL, FR_COUNT)
                mCONFIG.LOGGER.info("MODE_FACE_REGISTERING {}/{}".format(FR_COUNT, mCONFIG.FR_TOTAL))
                text = "Registering {}/{} images for [{}]".format(
                    FR_COUNT, mCONFIG.FR_TOTAL, FR_USER_ID)
                frame = cv2.putText(
                    frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                yield cv2.imencode('.jpg', frame)[1].tobytes()
                continue

            # 3. MODE_FACE_STREAMING
            # update recoginzing status
            if frame_count % (SKIP_FRAME_RECOGNIZING) == 0:
                FACE_RECOGNIZING = True
                print("Training status: ", mCONFIG.TRAINING_STATUS)
                AILIBS.update(mCONFIG.TRAINING_STATUS)

            # 4. MODE_FACE_TRACKING
            # update recoginzing status
            if frame_count % (SKIP_FRAME_TRACKING) == 0:
                FACE_TRACKING = True

            # detecting face features
            dets = []
            if mAILIBS.DETECTOR is not None:
                dets = mAILIBS.DETECTOR.detect(temp)

            # update tracker
            face_trackers = mAILIBS.TRACKERS.update(dets)

            # extracting face features
            features_list = []
            face_list = []
            raw_image = frame.copy()
            for d in dets:
                latest_updated = int(time())
                [left, top, right, bottom] = mAILIBS.DETECTOR.get_position(d)

                # cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 255))
                [t, l, r, b] = [max(0, top-int(2*FACE_PADDING)), max(0, left-FACE_PADDING), min(
                    right+FACE_PADDING, frame.shape[1]), min(bottom+FACE_PADDING, frame.shape[0])]
                cv2.rectangle(frame, (l, t), (r, b), (0, 255, 255), 2)
                if FACE_RECOGNIZING:
                    if mAILIBS.TRACKERS.check(d, NAME_LIST, ID):
                        features = mAILIBS.EXTRACTOR.extract(temp, d)
                        features_list.append(features)
                        face = raw_image[t:b, l:r]
                        face_list.append(face)

            # classifying face
            user_list = []
            if len(features_list) > 0:
                if mAILIBS.CLASSIFIER is None:
                    print("FACE_CLASSIFIER is None !")
                    continue
                user_list = mAILIBS.CLASSIFIER.classify_list(features_list)
                for i, user in enumerate(user_list):
                    if bool(user):
                        user['latest_time'] = int(time())
                        NAME_LIST[user['name']] = user
                        # frame = cv2.putText(
                        #     frame, user['name'], (left, top), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)
                        checkin = {"employee_id": user['name'],
                                   "start_time": int(time()),
                                   "end_time": int(time())}
                        DB_UPDATED_CHECKIN(checkin, face_list[i])
                while NOONE in user_list:
                    user_list.remove(NOONE)
                FACE_RECOGNIZING = False
                COUNTER = 0

            # track to verified user
            mAILIBS.TRACKERS.track_face(
                ID, trackcount, dets, user_list, NAME_LIST, line_track, FACE_TRACKING, frame)
            FACE_TRACKING = False
            if len(user_list) == 0:
                for i, d in enumerate(dets):
                    user = {}
                    user['name'] = "Unknown"
                    user['score'] = 0
                    user['lastest_time'] = 0
                    user_list.append(user)

            # update skipping frame for real-time streaming
            if len(dets) > 0:
                skip_step = SKIP_FRAME_DETECTING
            else:
                skip_step = SKIP_FRAME_STREAMING

            # clearing outdate user
            for key, value in list(NAME_LIST.items()):
                if mAILIBS.TRACKERS.exist(NAME_LIST[key], ID) is False:
                    mCONFIG.LOGGER.info("Cleaning...{} ".format(NAME_LIST[key]["name"]))
                    print('Cleaning', int(
                        time()) - NAME_LIST[key]["latest_time"], 'frame_count', frame_count, len(dets))
                    del NAME_LIST[key]
                    FACE_RECOGNIZING = True
                else:
                    mCONFIG.LOGGER.info("FC...{}- dets:{}- time {}- NAME_LIST: {}".format(frame_count, len(dets), str(int(time())), str(NAME_LIST)))
                    # print('Frame_count', frame_count, len(
                    #     dets), str(int(time())), NAME_LIST)

            frame = draw_frame(frame, frame_count, star_time,
                               NAME_LIST, line_track, face_trackers)
            yield cv2.imencode('.jpg', frame)[1].tobytes()
