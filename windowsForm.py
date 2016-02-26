# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'anacondaCasino.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setEnabled(True)
        MainWindow.resize(600, 480)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.frameLog = QtGui.QFrame(self.centralwidget)
        self.frameLog.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frameLog.setFrameShadow(QtGui.QFrame.Raised)
        self.frameLog.setObjectName(_fromUtf8("frameLog"))
        self.textEdit = QtGui.QTextEdit(self.frameLog)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 271, 401))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.textEdit.raise_()
        self.horizontalLayout.addWidget(self.frameLog)
        self.frameOperation = QtGui.QFrame(self.centralwidget)
        self.frameOperation.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frameOperation.setFrameShadow(QtGui.QFrame.Raised)
        self.frameOperation.setObjectName(_fromUtf8("frameOperation"))
        self.comboBoxDevice = QtGui.QComboBox(self.frameOperation)
        self.comboBoxDevice.setGeometry(QtCore.QRect(10, 10, 162, 20))
        self.comboBoxDevice.setObjectName(_fromUtf8("comboBoxDevice"))
        self.comboBoxDevice.addItem(_fromUtf8(""))
        self.spinBox_waitBase = QtGui.QSpinBox(self.frameOperation)
        self.spinBox_waitBase.setGeometry(QtCore.QRect(10, 54, 51, 20))
        self.spinBox_waitBase.setMaximum(3000)
        self.spinBox_waitBase.setSingleStep(100)
        self.spinBox_waitBase.setProperty("value", 1000)
        self.spinBox_waitBase.setObjectName(_fromUtf8("spinBox_waitBase"))
        self.label = QtGui.QLabel(self.frameOperation)
        self.label.setGeometry(QtCore.QRect(10, 36, 81, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalSlider_waitRandom = QtGui.QSlider(self.frameOperation)
        self.verticalSlider_waitRandom.setGeometry(QtCore.QRect(120, 80, 22, 84))
        self.verticalSlider_waitRandom.setMaximum(3000)
        self.verticalSlider_waitRandom.setSingleStep(50)
        self.verticalSlider_waitRandom.setProperty("value", 1000)
        self.verticalSlider_waitRandom.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_waitRandom.setObjectName(_fromUtf8("verticalSlider_waitRandom"))
        self.verticalSlider_waitBase = QtGui.QSlider(self.frameOperation)
        self.verticalSlider_waitBase.setGeometry(QtCore.QRect(20, 80, 22, 84))
        self.verticalSlider_waitBase.setMaximum(3000)
        self.verticalSlider_waitBase.setSingleStep(50)
        self.verticalSlider_waitBase.setProperty("value", 1000)
        self.verticalSlider_waitBase.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_waitBase.setObjectName(_fromUtf8("verticalSlider_waitBase"))
        self.spinBox_waitRandom = QtGui.QSpinBox(self.frameOperation)
        self.spinBox_waitRandom.setGeometry(QtCore.QRect(113, 54, 51, 20))
        self.spinBox_waitRandom.setMaximum(3000)
        self.spinBox_waitRandom.setSingleStep(100)
        self.spinBox_waitRandom.setProperty("value", 1000)
        self.spinBox_waitRandom.setObjectName(_fromUtf8("spinBox_waitRandom"))
        self.pushButtonRun = QtGui.QPushButton(self.frameOperation)
        self.pushButtonRun.setGeometry(QtCore.QRect(10, 330, 161, 81))
        self.pushButtonRun.setMinimumSize(QtCore.QSize(75, 23))
        self.pushButtonRun.setAutoRepeatDelay(300)
        self.pushButtonRun.setObjectName(_fromUtf8("pushButtonRun"))
        self.label_2 = QtGui.QLabel(self.frameOperation)
        self.label_2.setGeometry(QtCore.QRect(113, 36, 101, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.commandLinkButton = QtGui.QCommandLinkButton(self.frameOperation)
        self.commandLinkButton.setGeometry(QtCore.QRect(10, 280, 188, 41))
        self.commandLinkButton.setObjectName(_fromUtf8("commandLinkButton"))
        self.horizontalLayout.addWidget(self.frameOperation)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.pushButtonRun, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.runProgram)
        QtCore.QObject.connect(self.spinBox_waitBase, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.verticalSlider_waitBase.setValue)
        QtCore.QObject.connect(self.verticalSlider_waitRandom, QtCore.SIGNAL(_fromUtf8("sliderMoved(int)")), self.spinBox_waitRandom.setValue)
        QtCore.QObject.connect(self.spinBox_waitRandom, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.verticalSlider_waitRandom.setValue)
        QtCore.QObject.connect(self.verticalSlider_waitBase, QtCore.SIGNAL(_fromUtf8("sliderMoved(int)")), self.spinBox_waitBase.setValue)
        QtCore.QObject.connect(self.spinBox_waitBase, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), MainWindow.changeWaitBase)
        QtCore.QObject.connect(self.spinBox_waitRandom, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), MainWindow.changeWaitRandom)
        QtCore.QObject.connect(self.verticalSlider_waitBase, QtCore.SIGNAL(_fromUtf8("sliderMoved(int)")), MainWindow.changeWaitBase)
        QtCore.QObject.connect(self.verticalSlider_waitRandom, QtCore.SIGNAL(_fromUtf8("sliderMoved(int)")), MainWindow.changeWaitRandom)
        QtCore.QObject.connect(self.commandLinkButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.shortcutGrablu)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "AnacondaCasino", None))
        self.comboBoxDevice.setItemText(0, _translate("MainWindow", "<ネットワークデバイスの選択>", None))
        self.label.setText(_translate("MainWindow", "待ち時間基礎値", None))
        self.pushButtonRun.setText(_translate("MainWindow", "実行", None))
        self.label_2.setText(_translate("MainWindow", "待ち時間ランダム幅", None))
        self.commandLinkButton.setText(_translate("MainWindow", "グラブルを起動", None))

