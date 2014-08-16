# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_oceandata.ui'
#
# Created: Sat Aug 16 14:08:41 2014
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
        OceanData.resize(221, 267)
        self.label_2 = QtGui.QLabel(OceanData)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 62, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.spnEndDate = QtGui.QSpinBox(OceanData)
        self.spnEndDate.setGeometry(QtCore.QRect(150, 60, 61, 24))
        self.spnEndDate.setMinimum(2002)
        self.spnEndDate.setMaximum(2013)
        self.spnEndDate.setProperty("value", 2013)
        self.spnEndDate.setObjectName(_fromUtf8("spnEndDate"))
        self.spnStartDate = QtGui.QSpinBox(OceanData)
        self.spnStartDate.setGeometry(QtCore.QRect(80, 60, 61, 24))
        self.spnStartDate.setMinimum(2002)
        self.spnStartDate.setMaximum(2013)
        self.spnStartDate.setProperty("value", 2002)
        self.spnStartDate.setObjectName(_fromUtf8("spnStartDate"))
        self.txtPath = QtGui.QLineEdit(OceanData)
        self.txtPath.setGeometry(QtCore.QRect(10, 30, 201, 21))
        self.txtPath.setObjectName(_fromUtf8("txtPath"))
        self.plainTextEdit = QtGui.QPlainTextEdit(OceanData)
        self.plainTextEdit.setEnabled(False)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 90, 201, 131))
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.label = QtGui.QLabel(OceanData)
        self.label.setGeometry(QtCore.QRect(10, 10, 62, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.btnDownload = QtGui.QPushButton(OceanData)
        self.btnDownload.setGeometry(QtCore.QRect(100, 230, 114, 32))
        self.btnDownload.setObjectName(_fromUtf8("btnDownload"))

        self.retranslateUi(OceanData)
        QtCore.QObject.connect(self.btnDownload, QtCore.SIGNAL(_fromUtf8("clicked()")), OceanData.accept)
        QtCore.QMetaObject.connectSlotsByName(OceanData)

    def retranslateUi(self, OceanData):
        OceanData.setWindowTitle(_translate("OceanData", "OceanData", None))
        self.label_2.setText(_translate("OceanData", "Range:", None))
        self.txtPath.setText(_translate("OceanData", "/Users/Ireland/rsr/qgis-dev/", None))
        self.label.setText(_translate("OceanData", "Path", None))
        self.btnDownload.setText(_translate("OceanData", "Download", None))

