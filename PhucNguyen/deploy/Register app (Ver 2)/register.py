from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from pydub import AudioSegment

# import Opencv module
import cv2
import sys
import dlib
import numpy as np
import imutils
# import tensorflow as tf
import os
import argparse
# import Opencv module
import pyaudio
import wave
import argparse
from io import BytesIO
import pickle
import librosa
import resemblyzer
import shutil

# GUI of register app
from ui_inputWindow import *
from ui_faceWindow import *
from ui_voiceWindow import *
from ui_openWindow import *

# Library for face detection
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')

# Create place for storing temporary ID 
if not os.path.exists('data'):
    os.makedirs('data')
with open('data/ID.txt', 'w') as f:
    f.write("")

# First window for filling ID
class InputWindow(QMainWindow):
    switch_window = QtCore.pyqtSignal()
    switch_openWindow = QtCore.pyqtSignal()
    # class constructor
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.ui = Ui_InputWindow()
        self.ui.setupUi(self)
        # Disable next button when nothing fill in ID box
        self.ui.NextButton.setEnabled(False)
        self.ui.inputID.setText("")
        # Disable New in menubar until temporary ID exist
        self.ui.new_act.setEnabled(False)
        # Disable Save in menubar until process done
        self.ui.save_act.setEnabled(False)
        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function that check temporary ID
        self.timer.timeout.connect(self.checkInput)
        self.timer.start(20)

        # Click next button
        self.ui.NextButton.clicked.connect(self.pushbutton_handler1)
        # Open file menu and click New (Ctrl + N)
        self.ui.new_act.triggered.connect(self.setNew)
        # Open file menu and click Open (Ctrl + O)
        self.ui.open_act.triggered.connect(self.openUser)
        # Open file menu and click Save (Ctrl + S)
        self.ui.save_act.triggered.connect(self.saveUser)
        # Open file menu and click Exit (Ctrl + Esc)
        self.ui.exit_act.triggered.connect(self.closeApp)

    def checkInput(self):
        # if temporary ID exists in ID.txt, the Next button will appear
        if self.ui.inputID.text() != "":
            self.ui.NextButton.setEnabled(True)
        else:
            self.ui.NextButton.setEnabled(False)

        # if temporary ID exist in "ID.txt", new user in menubar will be enabled
        with open('data/ID.txt', 'r') as f:
                ID = f.read()
        if ID != "":
            self.ui.new_act.setEnabled(True)
            # If process done, save in menubar will be enabled
            if os.path.exists(f'data/{ID}/voice/3.wav'):
                self.ui.save_act.setEnabled(True)
            else:
                self.ui.save_act.setEnabled(False) # else it still be disabled
            self.ui.inputID.setText(ID)
        else:
            self.ui.new_act.setEnabled(False) # else create new in menubar will be disabled



    def pushbutton_handler1(self):
        # Create place for storing face data and voice data
        ID = self.ui.inputID.text()
        if not os.path.exists(f'data/{ID}/voice'):
            os.makedirs(f'data/{ID}/voice')
        if not os.path.exists(f'data/{ID}/face'):
            os.makedirs(f'data/{ID}/face')

        # Save ID to temporary place "ID.txt"
        with open(f'data/ID.txt', 'w') as f:
            f.write(ID)
        # Go to next face window
        self.switch_window.emit()


#Function of menubar
 
    def setNew(self):
        # Pop up message box when exit. 2 option yes or no
        reply = QMessageBox.question(self,'Message','Press Yes to create New user.',QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        
        if reply == QMessageBox.Yes:
            # When face data and voice data have not done, 
            # click yes will lead to remove current ID folder
            with open('data/ID.txt', 'r') as f:
                ID = f.read()
            if not os.path.exists(f'data/{ID}/voice/3.wav'):
                shutil.rmtree(f'data/{ID}', ignore_errors=True)
            # Clear temporary ID
            with open('data/ID.txt', 'w') as f:
                f.write("")
        if reply == QMessageBox.No:
            return

    def openUser(self):
        # Go to open window 
        self.switch_openWindow.emit()

    def saveUser(self):
        # Pop up message box when exit. 2 option yes or no
        reply = QMessageBox.question(self,'Message','Press Yes to save user.',QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        
        if reply == QMessageBox.Yes:
            with open('data/ID.txt', 'r') as f:
                ID = f.read()
            # Clear temporary ID
            with open('data/ID.txt', 'w') as f:
                f.write("")
        if reply == QMessageBox.No:
            return

    def closeApp(self):
        # Pop up message box when exit. 2 option yes or no
        reply = QMessageBox.question(self,'Message','Press Yes to Close.',QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        
        if reply == QMessageBox.Yes:
            # When face data and voice data have not done, 
            # click yes will lead to remove current ID folder
            with open('data/ID.txt', 'r') as f:
                ID = f.read()
            if ID != "":
                if not os.path.exists(f'data/{ID}/voice/3.wav'):
                    shutil.rmtree(f'data/{ID}', ignore_errors=True)
            sys.exit()
        if reply == QMessageBox.No:
            return


class FaceWindow(QMainWindow):
    switch_window1 = QtCore.pyqtSignal() # link to input window
    switch_window2 = QtCore.pyqtSignal() # link to voice window

    switch_openWindow = QtCore.pyqtSignal()
    # class constructor
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.ui = Ui_FaceWindow()
        self.ui.setupUi(self)
        self.ID = ""
        self.count = 0 # use for count taken photo
        self.picCheck = 0 # use for displaying 10 photos each time
        self.progress = 0 # Use for displaying number of photo
        self.ui.count_label.setText("0/0")
        # Disable next window until taking 100 photos
        self.ui.next_bt.setEnabled(False)
        # Disable Save in menubar until process done
        self.ui.save_act.setEnabled(False)

        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)
        self.cap = cv2.VideoCapture(0)
        self.timer.start(20)

        # Initialize the taking photo
        self.ui.record_bt.clicked.connect(lambda: self.setCount(100))

        # Check face photo, 10 photos each time
        self.ui.forward_bt.clicked.connect(self.setForward)
        self.ui.back_bt.clicked.connect(self.setBack)

        # Previous window is input window, next window is voice window
        self.ui.previous_bt.clicked.connect(self.pushbutton_handler1)
        self.ui.next_bt.clicked.connect(self.pushbutton_handler2)

        # Open file menu and click New (Ctrl + N)
        self.ui.new_act.triggered.connect(self.setNew)
        # Open file menu and click Open (Ctrl + O)
        self.ui.open_act.triggered.connect(self.openUser)
        # Open file menu and click Save (Ctrl + S)
        self.ui.save_act.triggered.connect(self.saveUser)
        # Open file menu and click Exit (Ctrl + Esc)
        self.ui.exit_act.triggered.connect(self.closeApp)

    def pushbutton_handler1(self):
        self.switch_window1.emit() # Go to input window

    def pushbutton_handler2(self):
        self.switch_window2.emit() # Go to voice window

    # Initialize the taking photo
    def setCount(self, item): 
        self.count = item
        self.check = True
        self.progress = 0

    # Check next 10 photos
    def setForward(self):
        if self.picCheck<9:
            self.picCheck = self.picCheck + 1

    # Check back 10 photos
    def setBack(self):
        if self.picCheck>0:
            self.picCheck = self.picCheck - 1


    # view camera
    def viewCam(self):
        # Update ID in face window
        with open(f'data/ID.txt', 'r') as f:
            self.ID = f.read()

        # If process done, save in menubar will be enabled
        if os.path.exists(f'data/{self.ID}/voice/3.wav'):
            self.ui.save_act.setEnabled(True)
        else:
            self.ui.save_act.setEnabled(False) # else it still be disabled

        # If user already has 100 photos, system displays photo in check area
        if os.path.exists(f"data/{self.ID}/face/test100.jpg"):
            self.ui.next_bt.setEnabled(True)
            self.ui.count_label.setText(f"{(self.picCheck+1)*10}/100")
            w = self.ui.pic1_label.width()
            h = self.ui.pic1_label.height()
            self.ui.pic1_label.setPixmap(QtGui.QPixmap(f"data/{self.ID}/face/test{self.picCheck*10+1}.jpg").scaled(w, h, QtCore.Qt.KeepAspectRatio))
            self.ui.pic2_label.setPixmap(QtGui.QPixmap(f"data/{self.ID}/face/test{self.picCheck*10+2}.jpg").scaled(w, h, QtCore.Qt.KeepAspectRatio))
            self.ui.pic3_label.setPixmap(QtGui.QPixmap(f"data/{self.ID}/face/test{self.picCheck*10+3}.jpg").scaled(w, h, QtCore.Qt.KeepAspectRatio))
            self.ui.pic4_label.setPixmap(QtGui.QPixmap(f"data/{self.ID}/face/test{self.picCheck*10+4}.jpg").scaled(w, h, QtCore.Qt.KeepAspectRatio))
            self.ui.pic5_label.setPixmap(QtGui.QPixmap(f"data/{self.ID}/face/test{self.picCheck*10+5}.jpg").scaled(w, h, QtCore.Qt.KeepAspectRatio))
            self.ui.pic6_label.setPixmap(QtGui.QPixmap(f"data/{self.ID}/face/test{self.picCheck*10+6}.jpg").scaled(w, h, QtCore.Qt.KeepAspectRatio))
            self.ui.pic7_label.setPixmap(QtGui.QPixmap(f"data/{self.ID}/face/test{self.picCheck*10+7}.jpg").scaled(w, h, QtCore.Qt.KeepAspectRatio))
            self.ui.pic8_label.setPixmap(QtGui.QPixmap(f"data/{self.ID}/face/test{self.picCheck*10+8}.jpg").scaled(w, h, QtCore.Qt.KeepAspectRatio))
            self.ui.pic9_label.setPixmap(QtGui.QPixmap(f"data/{self.ID}/face/test{self.picCheck*10+9}.jpg").scaled(w, h, QtCore.Qt.KeepAspectRatio))
            self.ui.pic10_label.setPixmap(QtGui.QPixmap(f"data/{self.ID}/face/test{self.picCheck*10+10}.jpg").scaled(w, h, QtCore.Qt.KeepAspectRatio))
        else:
            # else set check area to empty
            self.ui.next_bt.setEnabled(False)
            self.picCheck = 0
            self.ui.count_label.setText("0/0")
            self.ui.pic1_label.setPixmap(QtGui.QPixmap(""))
            self.ui.pic2_label.setPixmap(QtGui.QPixmap(""))
            self.ui.pic3_label.setPixmap(QtGui.QPixmap(""))
            self.ui.pic4_label.setPixmap(QtGui.QPixmap(""))
            self.ui.pic5_label.setPixmap(QtGui.QPixmap(""))
            self.ui.pic6_label.setPixmap(QtGui.QPixmap(""))
            self.ui.pic7_label.setPixmap(QtGui.QPixmap(""))
            self.ui.pic8_label.setPixmap(QtGui.QPixmap(""))
            self.ui.pic9_label.setPixmap(QtGui.QPixmap(""))
            self.ui.pic10_label.setPixmap(QtGui.QPixmap(""))

        # Begin taking photo
        SCALE = 1
        
        # read image in BGR format
        ret, image = self.cap.read()
        temp = cv2.resize(image, (0, 0), fx=1/SCALE, fy=1/SCALE)
        dets = detector(image)
        # convert image to RGB format
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # get image infos
        height, width, channel = image.shape
        step = channel * width
            
        # create QImage from image
        qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        for d in dets:
            # self.timer.start(20)
            left = d.left()*SCALE
            right = d.right()*SCALE
            top = d.top()*SCALE
            bottom = d.bottom()*SCALE
            # name = 'Guest'
            face=temp[d.top():d.bottom(), d.left():d.right()]
            cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 0))
            if self.count>0:
                cv2.imwrite(f'data/{self.ID}/face/test{101-self.count}.jpg', face)
                self.count=self.count-1
                self.progress = self.progress+1

        # Display checking data
        if self.progress>0:
            self.ui.count_label.setText(f"{(self.picCheck+1)*10}/{self.progress}")
            w = self.ui.pic1_label.width()
            h = self.ui.pic1_label.height()
            self.ui.pic1_label.setPixmap(QtGui.QPixmap(f"data/{self.ID}/face/test{self.picCheck*10+1}.jpg").scaled(w, h, QtCore.Qt.KeepAspectRatio))
            self.ui.pic2_label.setPixmap(QtGui.QPixmap(f"data/{self.ID}/face/test{self.picCheck*10+2}.jpg").scaled(w, h, QtCore.Qt.KeepAspectRatio))
            self.ui.pic3_label.setPixmap(QtGui.QPixmap(f"data/{self.ID}/face/test{self.picCheck*10+3}.jpg").scaled(w, h, QtCore.Qt.KeepAspectRatio))
            self.ui.pic4_label.setPixmap(QtGui.QPixmap(f"data/{self.ID}/face/test{self.picCheck*10+4}.jpg").scaled(w, h, QtCore.Qt.KeepAspectRatio))
            self.ui.pic5_label.setPixmap(QtGui.QPixmap(f"data/{self.ID}/face/test{self.picCheck*10+5}.jpg").scaled(w, h, QtCore.Qt.KeepAspectRatio))
            self.ui.pic6_label.setPixmap(QtGui.QPixmap(f"data/{self.ID}/face/test{self.picCheck*10+6}.jpg").scaled(w, h, QtCore.Qt.KeepAspectRatio))
            self.ui.pic7_label.setPixmap(QtGui.QPixmap(f"data/{self.ID}/face/test{self.picCheck*10+7}.jpg").scaled(w, h, QtCore.Qt.KeepAspectRatio))
            self.ui.pic8_label.setPixmap(QtGui.QPixmap(f"data/{self.ID}/face/test{self.picCheck*10+8}.jpg").scaled(w, h, QtCore.Qt.KeepAspectRatio))
            self.ui.pic9_label.setPixmap(QtGui.QPixmap(f"data/{self.ID}/face/test{self.picCheck*10+9}.jpg").scaled(w, h, QtCore.Qt.KeepAspectRatio))
            self.ui.pic10_label.setPixmap(QtGui.QPixmap(f"data/{self.ID}/face/test{self.picCheck*10+10}.jpg").scaled(w, h, QtCore.Qt.KeepAspectRatio))


        # show image in img_label
        self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))


# Function of menubar

    def setNew(self):
        # Pop up message box when exit. 2 option yes or no
        reply = QMessageBox.question(self,'Message','Press Yes to create New user.',QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        
        if reply == QMessageBox.Yes:
            # When face data and voice data have not done, 
            # click yes will lead to remove current ID folder
            with open('data/ID.txt', 'r') as f:
                ID = f.read()
            if not os.path.exists(f'data/{ID}/voice/3.wav'):
                shutil.rmtree(f'data/{ID}', ignore_errors=True)
            # Clear temporary ID
            with open('data/ID.txt', 'w') as f:
                f.write("")
            # Go to first window 
            self.switch_window1.emit()
        if reply == QMessageBox.No:
            return

    def openUser(self):
        # Go to open window 
        self.switch_openWindow.emit()
        
    def saveUser(self):
        # Pop up message box when exit. 2 option yes or no
        reply = QMessageBox.question(self,'Message','Press Yes to save user.',QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        
        if reply == QMessageBox.Yes:
            with open('data/ID.txt', 'r') as f:
                ID = f.read()
            # Clear temporary ID
            with open('data/ID.txt', 'w') as f:
                f.write("")
            self.switch_window1.emit()
        if reply == QMessageBox.No:
            return

    def closeApp(self):
        reply = QMessageBox.question(self,'Message','Press Yes to Close.',QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        
        if reply == QMessageBox.Yes:
            # When face data and voice data have not done, 
            # click yes will lead to remove current ID folder
            with open('data/ID.txt', 'r') as f:
                ID = f.read()
            if ID != "":
                if not os.path.exists(f'data/{ID}/voice/3.wav'):
                    shutil.rmtree(f'data/{ID}', ignore_errors=True)
            sys.exit()
        if reply == QMessageBox.No:
            return

class VoiceWindow(QMainWindow):
    switch_window1 = QtCore.pyqtSignal()
    switch_window2 = QtCore.pyqtSignal()  
    switch_openWindow = QtCore.pyqtSignal()  # class constructor
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.ui = Ui_VoiceWindow()
        self.ui.setupUi(self)
        self.mic = []
        p1 = pyaudio.PyAudio()
        info = p1.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        self.ui.DeviceBox.setDuplicatesEnabled(False)
        for i in range(0, numdevices):
            self.mic.append(p1.get_device_info_by_host_api_device_index(0, i).get('name'))
            self.ui.DeviceBox.addItem(p1.get_device_info_by_host_api_device_index(0, i).get('name'))
        p1.terminate()
        self.ID=""
        self.CHUNK = 512
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.RECORD_SECONDS = 2
        self.player = QMediaPlayer()
        self.count = 0
        self.volume = 0
        self.player.setVolume(100)
        self.ui.record1_cb.setEnabled(False)
        self.ui.record2_cb.setEnabled(False)
        self.ui.record3_cb.setEnabled(False)
        self.ui.volume_sl.setMaximum(100)
        self.ui.volume_sl.setPageStep(1)
        self.ui.volume_sl.setValue(100)
        self.ui.play_bt.setEnabled(False)
        self.ui.done_bt.setEnabled(False)
        # Disable Save in menubar until process done
        self.ui.save_act.setEnabled(False)
    

        self.ui.record_sl.setRange(0,0)
        self.ui.record_sl.sliderMoved.connect(self.set_position)

        self.player.positionChanged.connect(self.position_changed)
        self.player.durationChanged.connect(self.duration_changed)
    
        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.recordHandler)
        self.timer.start(20)
        # set control_bt callback clicked  function

        self.ui.record_bt.clicked.connect(lambda: self.setCount(5))

        self.ui.volume_sl.valueChanged.connect(self.changeVolume)
        self.ui.play_bt.clicked.connect(self.playing)
        self.ui.previous_bt.clicked.connect(self.pushbutton_handler1)
        self.ui.done_bt.clicked.connect(self.pushbutton_handler2)
        # Open file menu and click New (Ctrl + N)
        self.ui.new_act.triggered.connect(self.setNew)
        # Open file menu and click Open (Ctrl + O)
        self.ui.open_act.triggered.connect(self.openUser)
        # Open file menu and click Save (Ctrl + S)
        self.ui.save_act.triggered.connect(self.saveUser)
        # Open file menu and click Exit (Ctrl + Esc)
        self.ui.exit_act.triggered.connect(self.closeApp)

    def pushbutton_handler1(self):
        self.switch_window1.emit()

    def pushbutton_handler2(self):
        with open('data/ID.txt', 'w') as f:
            f.write("")
        self.switch_window2.emit()

    def position_changed(self, position):
        self.ui.record_sl.setValue(position)
 
    def duration_changed(self, duration):
        self.ui.record_sl.setRange(0, duration)

    def set_position(self, position):
        self.player.setPosition(position)


    def setCount(self, item):
        self.count = item
        self.data_encode = []
        self.ui.record1_cb.setChecked(False)
        self.ui.record2_cb.setChecked(False)
        self.ui.record3_cb.setChecked(False)

    def setCountPlay(self, item):
        self.countPlay = item

    def changeVolume(self, value):
        self.player.setVolume(value)

    def playing(self):
        sound1 = AudioSegment.from_wav(f"data/{self.ID}/voice/1.wav")
        sound2 = AudioSegment.from_wav(f"data/{self.ID}/voice/2.wav")
        sound3 = AudioSegment.from_wav(f"data/{self.ID}/voice/3.wav")

        combined_sounds = sound1 + sound2 + sound3
        combined_sounds.export(f"data/{self.ID}/voice/joinedFile.wav", format="wav")
        filename = os.path.abspath(f"data/{self.ID}/voice/joinedFile.wav")
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
        self.player.play()


    # handle the record
    def recordHandler(self):
        mic1 = []
        p1 = pyaudio.PyAudio()
        info = p1.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        self.ui.DeviceBox.setDuplicatesEnabled(False)
        for i in range(0, numdevices):
            mic1.append(p1.get_device_info_by_host_api_device_index(0, i).get('name'))
        if mic1 != self.mic:
            print(True)
            self.ui.DeviceBox.clear()
            self.ui.DeviceBox.addItems(mic1)
            self.mic = mic1
        p1.terminate()
        print(self.ui.DeviceBox.currentIndex())
        with open(f'data/ID.txt', 'r') as f:
            self.ID = f.read()
        # If process done, save in menubar will be enabled
        if os.path.exists(f'data/{self.ID}/voice/3.wav'):
            self.ui.save_act.setEnabled(True)
        else:
            self.ui.save_act.setEnabled(False) # else it still be disabled

        # Check 3 wav files exist or not
        if os.path.exists(f'data/{self.ID}/voice/1.wav'):
            self.ui.record1_cb.setChecked(True)
        else:
            self.ui.record1_cb.setChecked(False)
        if os.path.exists(f'data/{self.ID}/voice/2.wav'):
            self.ui.record2_cb.setChecked(True)
        else:
            self.ui.record2_cb.setChecked(False)
        if os.path.exists(f'data/{self.ID}/voice/3.wav'):
            self.ui.record3_cb.setChecked(True)
            self.ui.play_bt.setEnabled(True)
            self.ui.done_bt.setEnabled(True)
        else:
            self.ui.record3_cb.setChecked(False)
            self.ui.play_bt.setEnabled(False)
            self.ui.done_bt.setEnabled(False)

        # Record voice 
        if (self.count>0) & (self.count<=4):
            p = pyaudio.PyAudio()

            stream = p.open(format=self.FORMAT,
                            channels=self.CHANNELS,
                            rate=self.RATE,
                            input=True,
                            frames_per_buffer=self.CHUNK,
                            input_device_index=self.ui.DeviceBox.currentIndex())

            self.ui.status_lb.setText(f"Status: * recording {5-self.count}")
            # 1 record turn will not be used 
            if (self.count!= 4):
                wave_output_filename = f"data/{self.ID}/voice/{4-self.count}.wav"
                frames = []

                # Check the record check box
                if self.count == 1:
                    self.ui.record3_cb.setChecked(True)
                    self.ui.play_bt.setEnabled(True)
                    self.ui.done_bt.setEnabled(True)
                if self.count == 2:
                    self.ui.record2_cb.setChecked(True)
                if self.count == 3:
                    self.ui.record1_cb.setChecked(True)
                for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
                    data = stream.read(self.CHUNK)
                    frames.append(data)
                
                stream.stop_stream()
                stream.close()
                p.terminate()
                buff = BytesIO()
                wf = wave.open(wave_output_filename, 'wb')
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(p.get_sample_size(self.FORMAT))
                wf.setframerate(self.RATE)
                wf.writeframes(b''.join(frames))
                wf.close()
                encoded_data = resemblyzer.preprocess_wav(wave_output_filename)
                self.data_encode.append(encoded_data)

                # Save pickle file
                with open(f'data/{self.ID}/voice/{self.ID}_encoded_wav.pickle', 'wb') as handle:
                    pickle.dump(self.data_encode, handle, protocol=pickle.HIGHEST_PROTOCOL)
            self.count -= 1
        if self.count == 0:
            # Status of not recording
            self.ui.status_lb.setText("Status: Click record")

        if self.count == 5:
            # Status of begin recording
            self.ui.status_lb.setText(f"Status: * Ready")
            self.count -= 1


# Function of menubar

    def setNew(self):
        # Pop up message box when exit. 2 option yes or no
        reply = QMessageBox.question(self,'Message','Press Yes to create New user.',QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        
        if reply == QMessageBox.Yes:
            # When face data and voice data have not done, 
            # click yes will lead to remove current ID folder
            with open('data/ID.txt', 'r') as f:
                ID = f.read()
            if not os.path.exists(f'data/{ID}/voice/3.wav'):
                shutil.rmtree(f'data/{ID}', ignore_errors=True)
            # Clear temporary ID
            with open('data/ID.txt', 'w') as f:
                f.write("")
            # Go to first window 
            self.switch_window2.emit()
        if reply == QMessageBox.No:
            return

    def openUser(self):
        # Go to open window 
        self.switch_openWindow.emit()

    def saveUser(self):
        # Pop up message box when exit. 2 option yes or no
        reply = QMessageBox.question(self,'Message','Press Yes to save user.',QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        
        if reply == QMessageBox.Yes:
            with open('data/ID.txt', 'r') as f:
                ID = f.read()
            # Clear temporary ID
            with open('data/ID.txt', 'w') as f:
                f.write("")
            self.switch_window2.emit()
        if reply == QMessageBox.No:
            return

    def closeApp(self):
        reply = QMessageBox.question(self,'Message','Press Yes to Close.',QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        
        if reply == QMessageBox.Yes:
            # When face data and voice data have not done, 
            # click yes will lead to remove current ID folder
            with open('data/ID.txt', 'r') as f:
                ID = f.read()
            if ID != "":
                if not os.path.exists(f'data/{ID}/voice/3.wav'):
                    print(ID)
                    shutil.rmtree(f'data/{ID}', ignore_errors=True)
            sys.exit()
        if reply == QMessageBox.No:
            return

class OpenWindow(QMainWindow):
    # class constructor
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.ui = Ui_OpenWindow()
        self.ui.setupUi(self)
        # Get all existed ID to ID box
        self.listDir = os.listdir("data/")
        self.listDir.remove("ID.txt")
        for dir in self.listDir:
            if os.path.exists(f'data/{dir}/voice/3.wav'):
                self.ui.ID_cb.addItem(dir)
        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.openHandler)
        self.timer.start(10)

        self.ui.ok_bt.clicked.connect(self.chooseID)
        self.ui.close_bt.clicked.connect(self.closeWindow)
        

    def openHandler(self):
        # New ID will put to ID box periodly 20ms
        newList = os.listdir("data/")
        newList.remove("ID.txt")
        for dir in newList:
            if os.path.exists(f'data/{dir}/voice/3.wav'):
                if not dir in self.listDir:
                    self.ui.ID_cb.addItem(dir)
                    self.listDir.append(dir)

    def chooseID(self):
        # Pop up message box when open other user. 2 option yes or no
        reply = QMessageBox.question(self,'Message','Press Yes to open other user.',QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        
        if reply == QMessageBox.Yes:
            # When face data and voice data have not done, 
            # click yes will lead to remove current ID folder
            with open('data/ID.txt', 'r') as f:
                ID = f.read()
            if ID != "":
                if not os.path.exists(f'data/{ID}/voice/3.wav'):
                    shutil.rmtree(f'data/{ID}', ignore_errors=True)
                # Clear temporary ID
                with open('data/ID.txt', 'w') as f:
                    f.write("")
            # Go to open window 
            ID = self.ui.ID_cb.currentText()
            with open('data/ID.txt', 'w') as f:
                f.write(ID)
        self.close()
        if reply == QMessageBox.No:
            return
        

    def closeWindow(self):
        self.close()


class Controller:

    def __init__(self):
        self.input = InputWindow()
        self.face = FaceWindow()
        self.voice = VoiceWindow()
        self.open = OpenWindow()

    def input_win(self):
        # self.input = InputWindow()
        self.input.switch_window.connect(self.face_win)
        self.input.switch_openWindow.connect(self.open_win)
        self.face.close()
        self.voice.close()
        self.open.close()
        self.input.show()

    def face_win(self):
        self.face.switch_window1.connect(self.input_win)
        self.face.switch_window2.connect(self.voice_win)
        self.face.switch_openWindow.connect(self.open_win)
        self.input.close()
        self.voice.close()
        self.open.close()
        self.face.show()

    def voice_win(self):
        self.voice.switch_window1.connect(self.face_win)
        self.voice.switch_window2.connect(self.input_win)
        self.voice.switch_openWindow.connect(self.open_win)
        self.face.close()
        self.input.close()
        self.open.close()
        self.voice.show()

    def open_win(self):
        self.open.show()


def main():
    app = QApplication(sys.argv)
    controller = Controller()
    controller.input_win()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()