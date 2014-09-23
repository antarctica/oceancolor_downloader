# -*- coding: utf-8 -*-
"""
/***************************************************************************
 OceanDataDialog
                                 A QGIS plugin
 Download oceanographic datasets
                             -------------------
        begin                : 2014-08-13
        copyright            : (C) 2014 by Louise Ireland
        email                : louireland@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from downloader import downloader
import time

from PyQt4 import QtCore, QtGui
from ui_oceandata import Ui_OceanData
# create the dialog for zoom to point


class DownloadThread(QtCore.QThread):
    def __init__(self, path, mindate, maxdate, res, datatype):
        self.path    = path
        self.mindate = mindate.toPyDate()
        self.maxdate = maxdate.toPyDate()
	self.res     = res
	self.datatype = datatype
        QtCore.QThread.__init__(self)
 
    def __del__(self):
        self.wait()

    def log(self, text):
        self.emit( QtCore.SIGNAL('update(QString)'), text )
 
    def run(self):
        # import you
        self.log("Downloading to {}".format(self.path))
        self.log("Range {0}-{1}".format(self.mindate, self.maxdate))
        C = downloader.get(self.datatype)
	d = C(self.mindate, self.maxdate, self.res)
	x = d.download(self.path)
	self.log("g: {}".format(x))
	self.log("Downloaded to {}".format(self.path))
	self.log("max date: {}".format(self.maxdate))


class OceanDataDialog(QtGui.QDialog, Ui_OceanData):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

    def log(self, text):
        self.plainTextEdit.appendPlainText(text)

    def accept(self):
        mindate = self.startDate.date()
        maxdate = self.endDate.date()
        path    = self.txtPath.text()
        res     = self.spnRes.value()
	datatype = 'chl'

        self.downloadThread = DownloadThread(path, mindate, maxdate, res, datatype)
        self.connect(self.downloadThread, QtCore.SIGNAL("update(QString)"), self.log)
        self.downloadThread.start()




