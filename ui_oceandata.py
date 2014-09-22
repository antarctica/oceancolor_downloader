# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_oceandata.ui'
#
# Created: Tue Sep 23 00:03:38 2014
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
        OceanData.resize(310, 369)
        self.label_2 = QtGui.QLabel(OceanData)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 62, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.txtPath = QtGui.QLineEdit(OceanData)
        self.txtPath.setGeometry(QtCore.QRect(10, 30, 291, 21))
        self.txtPath.setObjectName(_fromUtf8("txtPath"))
        self.plainTextEdit = QtGui.QPlainTextEdit(OceanData)
        self.plainTextEdit.setEnabled(False)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 180, 291, 131))
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.label = QtGui.QLabel(OceanData)
        self.label.setGeometry(QtCore.QRect(10, 10, 62, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.btnDownload = QtGui.QPushButton(OceanData)
        self.btnDownload.setGeometry(QtCore.QRect(100, 330, 114, 32))
        self.btnDownload.setObjectName(_fromUtf8("btnDownload"))
        self.startDate = QtGui.QDateEdit(OceanData)
        self.startDate.setGeometry(QtCore.QRect(70, 60, 111, 24))
        self.startDate.setObjectName(_fromUtf8("startDate"))
        self.endDate = QtGui.QDateEdit(OceanData)
        self.endDate.setGeometry(QtCore.QRect(190, 60, 111, 24))
        self.endDate.setDate(QtCore.QDate(2000, 1, 20))
        self.endDate.setObjectName(_fromUtf8("endDate"))
        self.spnRes = QtGui.QSpinBox(OceanData)
        self.spnRes.setGeometry(QtCore.QRect(90, 100, 49, 24))
        self.spnRes.setMinimum(4)
        self.spnRes.setMaximum(9)
        self.spnRes.setSingleStep(5)
        self.spnRes.setObjectName(_fromUtf8("spnRes"))
        self.label_3 = QtGui.QLabel(OceanData)
        self.label_3.setGeometry(QtCore.QRect(10, 100, 62, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))

        self.retranslateUi(OceanData)
        QtCore.QObject.connect(self.btnDownload, QtCore.SIGNAL(_fromUtf8("clicked()")), OceanData.accept)
        QtCore.QMetaObject.connectSlotsByName(OceanData)

    def retranslateUi(self, OceanData):
        OceanData.setWindowTitle(_translate("OceanData", "OceanData", None))
        self.label_2.setText(_translate("OceanData", "Range:", None))
        self.txtPath.setText(_translate("OceanData", "/Users/Ireland/rsr/qgis-dev/", None))
        self.label.setText(_translate("OceanData", "Path", None))
        self.btnDownload.setText(_translate("OceanData", "Download", None))
        self.startDate.setDisplayFormat(_translate("OceanData", "dd-MM-yyyy", None))
        self.endDate.setDisplayFormat(_translate("OceanData", "dd-MM-yyyy", None))
        self.label_3.setText(_translate("OceanData", "Resolution", None))

