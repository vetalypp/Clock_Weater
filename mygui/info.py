# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/vetaly/Dropbox/dev/PycharmProjects/info.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Info(object):
    def setupUi(self, Clock):
        Clock.setObjectName("Clock")
        Clock.resize(320, 240)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(149, 149, 149))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        Clock.setPalette(palette)
        Clock.setCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
        Clock.setAutoFillBackground(True)
        self.ssid = QtWidgets.QLabel(Clock)
        self.ssid.setGeometry(QtCore.QRect(23, 16, 281, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.ssid.setFont(font)
        self.ssid.setAlignment(QtCore.Qt.AlignCenter)
        self.ssid.setObjectName("ssid")

        self.retranslateUi(Clock)
        QtCore.QMetaObject.connectSlotsByName(Clock)

    def retranslateUi(self, Clock):
        _translate = QtCore.QCoreApplication.translate
        Clock.setWindowTitle(_translate("Clock", "Form"))
        self.ssid.setText(_translate("Clock", "Text"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Clock = QtWidgets.QWidget()
    ui = Ui_Clock()
    ui.setupUi(Clock)
    Clock.show()
    sys.exit(app.exec_())

