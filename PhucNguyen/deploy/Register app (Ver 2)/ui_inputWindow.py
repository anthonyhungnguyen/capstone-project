# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_inputWindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_InputWindow(object):
    def setupUi(self, InputWindow):
        InputWindow.setObjectName("InputWindow")
        InputWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(InputWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 6, 0, 1, 1)
        self.Title = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Title.setFont(font)
        self.Title.setTextFormat(QtCore.Qt.PlainText)
        self.Title.setAlignment(QtCore.Qt.AlignCenter)
        self.Title.setObjectName("Title")
        self.gridLayout.addWidget(self.Title, 1, 0, 1, 3)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 6, 2, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 4, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.ID = QtWidgets.QLabel(self.centralwidget)
        self.ID.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ID.setObjectName("ID")
        self.horizontalLayout.addWidget(self.ID)
        self.inputID = QtWidgets.QLineEdit(self.centralwidget)
        self.inputID.setObjectName("inputID")
        self.horizontalLayout.addWidget(self.inputID)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 3)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem5, 7, 1, 1, 1)
        self.NextButton = QtWidgets.QPushButton(self.centralwidget)
        self.NextButton.setObjectName("NextButton")
        self.gridLayout.addWidget(self.NextButton, 6, 1, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem6, 2, 0, 1, 3)
        InputWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(InputWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        InputWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(InputWindow)
        self.statusbar.setObjectName("statusbar")
        InputWindow.setStatusBar(self.statusbar)
        self.new_act = QtWidgets.QAction(InputWindow)
        self.new_act.setObjectName("new_act")
        self.open_act = QtWidgets.QAction(InputWindow)
        self.open_act.setObjectName("open_act")
        self.save_act = QtWidgets.QAction(InputWindow)
        self.save_act.setObjectName("save_act")
        self.exit_act = QtWidgets.QAction(InputWindow)
        self.exit_act.setObjectName("exit_act")
        self.commit_act = QtWidgets.QAction(InputWindow)
        self.commit_act.setObjectName("commit_act")
        self.menuFile.addAction(self.new_act)
        self.menuFile.addAction(self.open_act)
        self.menuFile.addAction(self.save_act)
        self.menuFile.addAction(self.commit_act)
        self.menuFile.addAction(self.exit_act)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(InputWindow)
        QtCore.QMetaObject.connectSlotsByName(InputWindow)

    def retranslateUi(self, InputWindow):
        _translate = QtCore.QCoreApplication.translate
        InputWindow.setWindowTitle(_translate("InputWindow", "MainWindow"))
        self.Title.setText(_translate("InputWindow", "Information register"))
        self.ID.setText(_translate("InputWindow", "Student ID"))
        self.NextButton.setText(_translate("InputWindow", "Next"))
        self.menuFile.setTitle(_translate("InputWindow", "File"))
        self.new_act.setText(_translate("InputWindow", "New"))
        self.new_act.setShortcut(_translate("InputWindow", "Ctrl+N"))
        self.open_act.setText(_translate("InputWindow", "Open"))
        self.open_act.setShortcut(_translate("InputWindow", "Ctrl+O"))
        self.save_act.setText(_translate("InputWindow", "Save"))
        self.save_act.setShortcut(_translate("InputWindow", "Ctrl+S"))
        self.exit_act.setText(_translate("InputWindow", "Exit"))
        self.exit_act.setShortcut(_translate("InputWindow", "Ctrl+Esc"))
        self.commit_act.setText(_translate("InputWindow", "Commit"))
        self.commit_act.setShortcut(_translate("InputWindow", "Ctrl+C"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    InputWindow = QtWidgets.QMainWindow()
    ui = Ui_InputWindow()
    ui.setupUi(InputWindow)
    InputWindow.show()
    sys.exit(app.exec_())
