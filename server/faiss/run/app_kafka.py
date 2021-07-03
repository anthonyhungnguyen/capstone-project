# PyQt5 libs
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt, QUrl

# import libs
import os
import cv2
import sys
import dlib
import numpy as np
import imutils
from dateutil.tz import gettz
from datetime import datetime
from time import time, localtime, strftime, sleep

from __init__ import PYTHON_PATH

# GUI of register app
from UI.ui import *

# import utils libs
from utils.AIlibs import AILIBS
mAILIBS = AILIBS

# Configuration networks, kafka
from utils.CONFIG import config
mCONFIG = config()

# Check frontal face
from ailibs.utilities.FaceUtilities import FaceUtilities as UTILS
mUTILS = UTILS

SIZE = (1152, 864)
CHECKED_SIZE = (211, 288)
SCALE = 1
FACE_PADDING = 15
NAME_LIST = {}
CHECKED_LIST = {}
UNKNOWN = "Unknown"
CHECKIN = "checkin"
CORRECT = "Thank you!\n"
WRONG = "Your info will \n be fixed soon!"
RESULT = ""
SCALE_H = 0.1
SCALE_W = 0.28
CHECKED_PATH = os.path.join(PYTHON_PATH, "ailibs_data/log/image/frame.jpg")
VECTOR_PATH = os.path.join(PYTHON_PATH, "ailibs_data", "classifier", "faiss", "vector.index")
INDEX_PATH = os.path.join(PYTHON_PATH, "ailibs_data", "classifier", "faiss", "index.npy")
THRES_PATH = os.path.join(PYTHON_PATH, "ailibs_data", "classifier", "faiss", "threshold.npy")
STREAM_PATH = 2
# STREAM_PATH = "/home/hoangphuc/Documents/semester202/thesis/deploy/test/video/test0.MOV"
# STREAM_PATH = "/home/hoangphuc/Documents/semester202/thesis/deploy/test/image/dat.jpg"


class MainWindow(QMainWindow):
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.device_label.setText("DEVICE: 1")
        self.ui.yes_button.setEnabled(False)
        self.ui.no_button.setEnabled(False)
        # create a timer
        self.timer = QTimer()
        # set camera
        self.cap = cv2.VideoCapture(STREAM_PATH)
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)
        self.timer.start(20)

        # Click Yes
        self.ui.yes_button.clicked.connect(self.checking_correct)

        # Click No
        self.ui.no_button.clicked.connect(self.checking_wrong)

    # view camera
    def viewCam(self):
        mCONFIG.schedule()
        mCONFIG.update()
        RESULT = mCONFIG.attendance_result()
        ret, frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        print(time()*1000)
        if not ret:
            return
        if mCONFIG.check_status() == CHECKIN:
            
            # crop [t:b, l:r]
            TOP = int(frame.shape[0]*SCALE_H)
            BOTTOM = frame.shape[0] - TOP
            LEFT = int(frame.shape[1]*SCALE_W)
            RIGHT = frame.shape[1] - LEFT
            # cv2.rectangle(frame, (LEFT, TOP),
            #               (RIGHT, BOTTOM), (200, 150, 150), 2)

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
                        NAME_LIST[CHECKED_LIST[trackID]['name']]['latest_time'] = int(time())
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
                        mCONFIG.checked_image(user['name'], features_list[i],check_frame)
                        CHECKED_LIST[trackID] = user
            elif len(trackers) > 0:
                if trackID in CHECKED_LIST:
                    NAME_LIST[CHECKED_LIST[trackID]['name']] = CHECKED_LIST[trackID]
            for key, value in list(NAME_LIST.items()):
                if int(time()) - NAME_LIST[key]["latest_time"] > 3:
                    mAILIBS.LOGGER.info(
                        "Cleaning...{} ".format(NAME_LIST[key]["name"]))
                    print('Cleaning', int(
                        time()) - NAME_LIST[key]["latest_time"], len(dets))
                    del NAME_LIST[key]
                    CHECKED_LIST.clear()
                    if os.path.exists(CHECKED_PATH):
                        os.remove(CHECKED_PATH) 
                else:
                    mAILIBS.LOGGER.info(
                        "dets:{}- time {}- NAME_LIST: {}".format(len(dets), str(int(time())), str(NAME_LIST)))

            flag = True
            for key in NAME_LIST:
                name = NAME_LIST[key]['name']
                if bool(CHECKED_LIST) or name != UNKNOWN:
                    flag = False
                    if self.ui.info_label.text() == CORRECT and RESULT != "":
                        print("*** RESULT: ", RESULT)
                        self.ui.info_label.setText(CORRECT + RESULT)
                    elif mCONFIG.check_time() and len(trackers) > 0 and trackID in CHECKED_LIST.keys():
                        self.ui.info_label.setText("Hello, {} \n {}".format(
                            CHECKED_LIST[trackID]['name'], strftime('%H:%M:%S', localtime(NAME_LIST[key]['latest_time']))))
                elif name == UNKNOWN:
                    flag = False
                    self.ui.info_label.setText("Unknown! \n {}".format(
                        strftime('%H:%M:%S', localtime(NAME_LIST[key]['latest_time']))))

            if flag:
                self.ui.info_label.setText("")
            course_info = mCONFIG.course_info()
            self.ui.course_label.setText(course_info)
            print(CHECKED_LIST)
        else:
            self.ui.info_label.setText("")
            self.ui.course_label.setText("")
            if os.path.exists(CHECKED_PATH):
                os.remove(CHECKED_PATH) 
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, SIZE)

        # get image infos
        height, width, channel = frame.shape
        step = channel * width

        # create QImage from image
        qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
        # show image in img_label
        self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))

        # show image in checked_area
        checked_image, flag = mCONFIG.get_checked_image()

        if flag:
            self.ui.yes_button.setEnabled(True)
            self.ui.no_button.setEnabled(True)
            checked_image = cv2.cvtColor(checked_image, cv2.COLOR_BGR2RGB)
            checked_image = cv2.resize(checked_image, CHECKED_SIZE)

            # get image infos
            height, width, channel = checked_image.shape
            step = channel * width

            # create QImage from image
            checked_qImg = QImage(checked_image.data, width, height, step, QImage.Format_RGB888)
            # show image in img_label
            self.ui.checked_label.setPixmap(QPixmap.fromImage(checked_qImg))
        else:
            self.ui.yes_button.setEnabled(False)
            self.ui.no_button.setEnabled(False)
            self.ui.checked_label.clear()
            

    def checking_correct(self):
        print("***** YES *******")
        mCONFIG.attendance(True)
        mCONFIG.lasted_checking()
        self.ui.info_label.setText(CORRECT)
        
    
    def checking_wrong(self):
        mCONFIG.attendance(False)
        mCONFIG.lasted_checking()
        self.ui.info_label.setText(WRONG)

def main():
    app = QApplication(sys.argv)
    controller = MainWindow()
    controller.showFullScreen()
    # controller.showMaximized()
    # controller.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
