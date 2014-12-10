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
    def __init__(self, path, mindate, maxdate, res, time_period, datatype):
        self.path    = '{}/'.format(path)
        self.mindate = mindate.toPyDate()
        self.maxdate = maxdate.toPyDate()
	self.res     = res
	self.datatype = datatype
	self.time_period = time_period
        
	QtCore.QThread.__init__(self)
 

    def __del__(self):
        self.wait()

    def log(self, text):
        self.emit( QtCore.SIGNAL('update(QString)'), text )
 
    def run(self):
	self.log("Dataset: {0}km {1} {2}".format(self.res, self.time_period, self.datatype))
	self.log("Range: {0} to {1}".format(self.mindate, self.maxdate))
	self.log("Downloading to: {}".format(self.path))
        C = downloader.get(self.datatype)
	d = C(self.mindate, self.maxdate, self.res, self.time_period)
	x = d.download(self.path)
	if x is not 0:
		for f in x:
			self.log("Failed: {}".format(f))
	self.log("Downloaded.".format(self.path))



class OceanDataDialog(QtGui.QDialog, Ui_OceanData):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
	self.data_desc = {
		'AQUA MODIS Chlorophyll Concentration': 'Mapped CHL-a concentrations \nValid date range: 2002/07/04 - present',
		'SeaWiFS Chlorophyll Concentration': 'Mapped CHL-a concentrations \nValid date range: 1997/09/04 - 2010/12/11',
		'Choose a dataset': '',
		'AQUA MODIS Sea Surface Temperature': 'Sea Surface Temps \nNot working yet.',
	}

    
    def log(self, text):
        self.plainTextEdit.appendPlainText(text)

    def show(self):
	self.plainTextEdit.clear()
	data_type = self.data_desc[self.comboBoxDatasets.currentText()]
	self.plainTextEdit.appendPlainText(data_type)
	
	self.comboBoxRes.clear()

	if self.comboBoxDatasets.currentText() == 'SeaWiFS Chlorophyll Concentration':
	    self.comboBoxRes.insertItem(0, '9km')
	    mindate = QtCore.QDate()
	    mindate.setDate(1997,9,4)
	    maxdate = QtCore.QDate()
	    maxdate.setDate(2010,12,11)
	    self.startDate.setDate(mindate)
	    self.endDate.setDate(maxdate)
	if self.comboBoxDatasets.currentText() == 'AQUA MODIS Chlorophyll Concentration':
	    self.comboBoxRes.insertItems(0, ['9km', '4km'])
	    mindate = QtCore.QDate()
	    mindate.setDate(2002,7,4)
	    maxdate = QtCore.QDate()
	    maxdate.setDate(2013,12,31)
	    self.startDate.setDate(mindate)
	    self.endDate.setDate(maxdate)
	if self.comboBoxDatasets.currentText() == 'AQUA MODIS Sea Surface Temperature':
	    self.comboBoxRes.insertItems(0, ['9km', '4km'])
	    mindate = QtCore.QDate()
	    mindate.setDate(2002,7,4)
	    maxdate = QtCore.QDate()
	    maxdate.setDate(2013,12,31)
	    self.startDate.setDate(mindate)
	    self.endDate.setDate(maxdate)


    def open(self):
	self.fileDialog = QtGui.QFileDialog(self)
	#self.fileDialog.show()
	self.txtPath.setText(self.fileDialog.getExistingDirectory())

    def accept(self):
        mindate  = self.startDate.date()
        maxdate  = self.endDate.date()
        path     = self.txtPath.text()
        res      = self.comboBoxRes.currentText()
	res      = int(res.replace('km', ''))
	datatype = self.comboBoxDatasets.currentText()
	period   = self.comboBoxTime.currentText()

        self.downloadThread = DownloadThread(path, mindate, maxdate, res, period, datatype)
        self.connect(self.downloadThread, QtCore.SIGNAL("update(QString)"), self.log)
        self.downloadThread.start()


