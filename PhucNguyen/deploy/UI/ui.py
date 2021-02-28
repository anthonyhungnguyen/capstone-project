# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_info.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1152, 864)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.image_label = QtWidgets.QLabel(self.groupBox)
        self.image_label.setGeometry(QtCore.QRect(0, 0, 1131, 821))
        self.image_label.setAutoFillBackground(True)
        self.image_label.setText("")
        self.image_label.setObjectName("image_label")
        self.info_label = QtWidgets.QLabel(self.groupBox)
        self.info_label.setGeometry(QtCore.QRect(40, 270, 251, 291))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(25)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.info_label.setFont(font)
        self.info_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.info_label.setAutoFillBackground(False)
        self.info_label.setStyleSheet("font: 57 25pt \"Ubuntu\";\n"
                                      "font-weight: bold;\n"
                                      "color: rgb(84, 0, 0);\n"
                                      "background-color : rgba(255, 255, 255, 90);")
        self.info_label.setText("")
        self.info_label.setAlignment(QtCore.Qt.AlignCenter)
        self.info_label.setObjectName("info_label")
        self.yes_button = QtWidgets.QPushButton(self.groupBox)
        self.yes_button.setGeometry(QtCore.QRect(940, 240, 151, 51))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.yes_button.setFont(font)
        self.yes_button.setObjectName("yes_button")
        self.face_label = QtWidgets.QLabel(self.groupBox)
        self.face_label.setGeometry(QtCore.QRect(240, 70, 651, 751))
        self.face_label.setText("")
        self.face_label.setPixmap(QtGui.QPixmap("UI/face.png"))
        self.face_label.setScaledContents(True)
        self.face_label.setObjectName("face_label")
        self.yes_button_2 = QtWidgets.QPushButton(self.groupBox)
        self.yes_button_2.setGeometry(QtCore.QRect(940, 500, 151, 51))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.yes_button_2.setFont(font)
        self.yes_button_2.setObjectName("yes_button_2")
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "GroupBox"))
        self.yes_button.setText(_translate("MainWindow", "YES"))
        self.yes_button_2.setText(_translate("MainWindow", "NO"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
