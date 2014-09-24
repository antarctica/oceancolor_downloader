# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_oceandata.ui'
#
# Created: Wed Sep 24 01:00:22 2014
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_OceanData(object):
    def setupUi(self, OceanData):
        OceanData.setObjectName(_fromUtf8("OceanData"))
        OceanData.resize(391, 369)
        self.label_2 = QtGui.QLabel(OceanData)
        self.label_2.setGeometry(QtCore.QRect(10, 100, 62, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.txtPath = QtGui.QLineEdit(OceanData)
        self.txtPath.setGeometry(QtCore.QRect(10, 70, 221, 21))
        self.txtPath.setObjectName(_fromUtf8("txtPath"))
        self.plainTextEdit = QtGui.QPlainTextEdit(OceanData)
        self.plainTextEdit.setEnabled(False)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 180, 351, 131))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.plainTextEdit.sizePolicy().hasHeightForWidth())
        self.plainTextEdit.setSizePolicy(sizePolicy)
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.label = QtGui.QLabel(OceanData)
        self.label.setGeometry(QtCore.QRect(10, 50, 62, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.btnDownload = QtGui.QPushButton(OceanData)
        self.btnDownload.setGeometry(QtCore.QRect(130, 330, 114, 32))
        self.btnDownload.setObjectName(_fromUtf8("btnDownload"))
        self.startDate = QtGui.QDateEdit(OceanData)
        self.startDate.setGeometry(QtCore.QRect(130, 100, 111, 24))
        self.startDate.setCalendarPopup(True)
        self.startDate.setObjectName(_fromUtf8("startDate"))
        self.endDate = QtGui.QDateEdit(OceanData)
        self.endDate.setGeometry(QtCore.QRect(250, 100, 111, 24))
        self.endDate.setCalendarPopup(True)
        self.endDate.setDate(QtCore.QDate(2000, 1, 20))
        self.endDate.setObjectName(_fromUtf8("endDate"))
        self.spnRes = QtGui.QSpinBox(OceanData)
        self.spnRes.setGeometry(QtCore.QRect(130, 140, 81, 24))
        self.spnRes.setMinimum(4)
        self.spnRes.setMaximum(9)
        self.spnRes.setSingleStep(5)
        self.spnRes.setObjectName(_fromUtf8("spnRes"))
        self.label_3 = QtGui.QLabel(OceanData)
        self.label_3.setGeometry(QtCore.QRect(10, 140, 62, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(OceanData)
        self.label_4.setGeometry(QtCore.QRect(10, 20, 62, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.comboBoxDatasets = QtGui.QComboBox(OceanData)
        self.comboBoxDatasets.setGeometry(QtCore.QRect(70, 10, 301, 26))
        self.comboBoxDatasets.setObjectName(_fromUtf8("comboBoxDatasets"))
        self.comboBoxDatasets.addItem(_fromUtf8(""))
        self.toolButton = QtGui.QToolButton(OceanData)
        self.toolButton.setGeometry(QtCore.QRect(250, 70, 27, 23))
        self.toolButton.setObjectName(_fromUtf8("toolButton"))

        self.retranslateUi(OceanData)
        QtCore.QObject.connect(self.btnDownload, QtCore.SIGNAL(_fromUtf8("clicked()")), OceanData.accept)
        QtCore.QObject.connect(self.toolButton, QtCore.SIGNAL(_fromUtf8("clicked()")), OceanData.open)
        QtCore.QMetaObject.connectSlotsByName(OceanData)

    def retranslateUi(self, OceanData):
        OceanData.setWindowTitle(_translate("OceanData", "OceanData", None))
        self.label_2.setText(_translate("OceanData", "Range:", None))
        self.txtPath.setText(_translate("OceanData", "/Users/Ireland/rsr/qgis-dev/", None))
        self.label.setText(_translate("OceanData", "Path", None))
        self.btnDownload.setText(_translate("OceanData", "Download", None))
        self.endDate.setDisplayFormat(_translate("OceanData", "dd-MM-yyyy", None))
        self.label_3.setText(_translate("OceanData", "Resolution", None))
        self.label_4.setText(_translate("OceanData", "Dataset", None))
        self.comboBoxDatasets.setItemText(0, _translate("OceanData", "AQUA MODIS Chlorophyll Concentration", None))
        self.toolButton.setText(_translate("OceanData", "...", None))

