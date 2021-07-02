import __init__

# PyQt5 libs
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt, QUrl

# GUI of register app
from UI.ui import *


# import libs
from time import time, localtime, strftime
import imutils
import numpy as np
import dlib
import sys
import cv2

# import utils libs
from utils.AIlibs import AILIBS

# Check frontal face
from ailibs.utilities.FaceUtilities import FaceUtilities as UTILS
mUTILS = UTILS

# Configuration networks, kafka
from utils.CONFIG import config
mCONFIG = config()


mAILIBS = AILIBS

SIZE = (1152, 864)
SCALE = 1
FACE_PADDING = 15
NAME_LIST = {}
CHECKED_LIST = {}
UNKNOWN = "Unknown"
SCALE_H = 0.1
SCALE_W = 0.28
STREAM_PATH = 0
# STREAM_PATH = "/home/hoangphuc/Documents/semester202/thesis/deploy/test/video/test0.MOV"
# STREAM_PATH = "/home/hoangphuc/Documents/semester202/thesis/deploy/test/image/dat.jpg"


class MainWindow(QMainWindow):
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # create a timer
        self.timer = QTimer()
        # set camera
        self.cap = cv2.VideoCapture(STREAM_PATH)
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)
        self.timer.start(20)

    # view camera
    def viewCam(self):
        ret, frame = self.cap.read()
        print("W:", frame.shape[0], "H:", frame.shape[1])
        if not ret:
            return
        # crop [t:b, l:r]
        TOP = int(frame.shape[0]*SCALE_H)
        BOTTOM = frame.shape[0] - TOP
        LEFT = int(frame.shape[1]*SCALE_W)
        RIGHT = frame.shape[1] - LEFT
        # cv2.rectangle(frame, (LEFT, TOP),
        #               (RIGHT, BOTTOM), (200, 150, 150), 2)
        # frame = cv2.flip(frame, 1)

        check_frame = frame[TOP:BOTTOM, LEFT:RIGHT]
        img_size = np.asarray(check_frame.shape)[0:2]

        dets = mAILIBS.DETECTOR.detect(check_frame)

        # extracting face features
        features_list = []
        face_list = []
        extract_flag = False

        for d in dets:
            [left, top, right, bottom] = mAILIBS.DETECTOR.get_position(d)
            item = [left, top, right, bottom]
            face_list.append(item)
            break
        final_faces = np.array(face_list)
        trackers = mAILIBS.TRACKER.update(final_faces, img_size)
        if len(trackers) > 0:
            trackID = trackers[0][4]
        if len(trackers) > 0:
            if trackID not in CHECKED_LIST.keys() and not bool(CHECKED_LIST):
                extract_flag = True
            elif trackID in CHECKED_LIST.keys():
                if CHECKED_LIST[trackID]['name'] == UNKNOWN:
                    extract_flag = True
                else:
                    NAME_LIST[CHECKED_LIST[trackID]['name']
                              ]['latest_time'] = int(time())
                    extract_flag = False
            else:
                # NAME_LIST[CHECKED_LIST[trackID]['name']]['latest_time'] = int(time())
                extract_flag = True
        if extract_flag:
            for d in dets:
                if mUTILS.is_frontal_face(check_frame, d, mAILIBS.EXTRACTOR):
                    # Features Extraction
                    features = mAILIBS.EXTRACTOR.extract(check_frame, d)
                    features_list.append(features)
                break
        if len(features_list) > 0:
            user_list = mAILIBS.CLASSIFIER.classify_list(features_list)
            for i, user in enumerate(user_list):
                user['latest_time'] = int(time())
                NAME_LIST[user['name']] = user
                if user['name'] != UNKNOWN:
                    mCONFIG.checked_image(
                        user['name'], features_list[i], check_frame)
                    CHECKED_LIST[trackID] = user
        elif len(trackers) > 0:
            if trackID in CHECKED_LIST:
                NAME_LIST[CHECKED_LIST[trackID]
                          ['name']] = CHECKED_LIST[trackID]
        for key, value in list(NAME_LIST.items()):
            if int(time()) - NAME_LIST[key]["latest_time"] > 3:
                mAILIBS.LOGGER.info(
                    "Cleaning...{} ".format(NAME_LIST[key]["name"]))
                print('Cleaning', int(
                    time()) - NAME_LIST[key]["latest_time"], len(dets))
                del NAME_LIST[key]
                CHECKED_LIST.clear()
            else:
                mAILIBS.LOGGER.info(
                    "dets:{}- time {}- NAME_LIST: {}".format(len(dets), str(int(time())), str(NAME_LIST)))
        flag = True
        for key in NAME_LIST:
            name = NAME_LIST[key]['name']
            if bool(CHECKED_LIST) or name != UNKNOWN:
                flag = False
                self.ui.info_label.setText("Hello, {} \n {}".format(
                    name, strftime('%H:%M:%S', localtime(NAME_LIST[key]['latest_time']))))
            elif name == UNKNOWN:
                flag = False
                self.ui.info_label.setText("Unknown! \n {}".format(
                    strftime('%H:%M:%S', localtime(NAME_LIST[key]['latest_time']))))

        if flag:
            self.ui.info_label.setText("")

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, SIZE)

        # get image infos
        height, width, channel = frame.shape
        step = channel * width

        # create QImage from image
        qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
        # show image in img_label
        self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))


def main():
    app = QApplication(sys.argv)
    controller = MainWindow()
    # controller.showFullScreen()
    # controller.showMaximized()
    controller.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
