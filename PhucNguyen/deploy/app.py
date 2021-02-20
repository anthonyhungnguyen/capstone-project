# PyQt5 libs
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt, QUrl

# GUI of register app
from ui import *

# import Opencv module
import cv2
import sys
import dlib
import numpy as np
import imutils

SIZE = (1152, 864)

class MainWindow(QMainWindow):
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)
        self.cap = cv2.VideoCapture(0)
        self.timer.start(20)

    # view camera
    def viewCam(self):
        _, image = self.cap.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, SIZE)
        image = cv2.flip(image, 1)
        # get image infos
        height, width, channel = image.shape
        step = channel * width
            
        # create QImage from image
        qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        # show image in img_label
        self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))

def main():
    app = QApplication(sys.argv)
    controller = MainWindow()
    controller.showFullScreen()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()