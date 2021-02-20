# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_openWindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_OpenWindow(object):
    def setupUi(self, OpenWindow):
        OpenWindow.setObjectName("OpenWindow")
        OpenWindow.resize(489, 378)
        self.centralwidget = QtWidgets.QWidget(OpenWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.close_bt = QtWidgets.QPushButton(self.centralwidget)
        self.close_bt.setObjectName("close_bt")
        self.horizontalLayout.addWidget(self.close_bt)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.ok_bt = QtWidgets.QPushButton(self.centralwidget)
        self.ok_bt.setObjectName("ok_bt")
        self.horizontalLayout.addWidget(self.ok_bt)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 0, 1, 2)
        self.ID_lb = QtWidgets.QLabel(self.centralwidget)
        self.ID_lb.setAlignment(QtCore.Qt.AlignCenter)
        self.ID_lb.setObjectName("ID_lb")
        self.gridLayout.addWidget(self.ID_lb, 1, 0, 1, 2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.ID_cb = QtWidgets.QComboBox(self.centralwidget)
        self.ID_cb.setObjectName("ID_cb")
        self.horizontalLayout_3.addWidget(self.ID_cb)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 2)
        spacerItem3 = QtWidgets.QSpacerItem(471, 111, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 3, 0, 1, 2)
        spacerItem4 = QtWidgets.QSpacerItem(471, 111, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem4, 0, 0, 1, 2)
        OpenWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(OpenWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 489, 22))
        self.menubar.setObjectName("menubar")
        OpenWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(OpenWindow)
        self.statusbar.setObjectName("statusbar")
        OpenWindow.setStatusBar(self.statusbar)

        self.retranslateUi(OpenWindow)
        QtCore.QMetaObject.connectSlotsByName(OpenWindow)

    def retranslateUi(self, OpenWindow):
        _translate = QtCore.QCoreApplication.translate
        OpenWindow.setWindowTitle(_translate("OpenWindow", "MainWindow"))
        self.close_bt.setText(_translate("OpenWindow", "Close"))
        self.ok_bt.setText(_translate("OpenWindow", "OK"))
        self.ID_lb.setText(_translate("OpenWindow", "Choose ID"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    OpenWindow = QtWidgets.QMainWindow()
    ui = Ui_OpenWindow()
    ui.setupUi(OpenWindow)
    OpenWindow.show()
    sys.exit(app.exec_())
