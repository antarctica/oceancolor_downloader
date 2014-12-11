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
from datetime import datetime
from PyQt4 import QtCore, QtGui
from ui_oceandata import Ui_OceanData
from qgis.utils import iface
from downloader import style_pick 
import os
# create the dialog for zoom to point



class DownloadThread(QtCore.QThread):
    def __init__(self, path, mindate, maxdate, res, time_period, datatype):
        self.path    = '{}/'.format(path)
        self.mindate = mindate.toPyDate()
	self.mindate = datetime.combine(self.mindate, datetime.min.time())
        self.maxdate = maxdate.toPyDate()
	self.maxdate = datetime.combine(self.maxdate, datetime.min.time())
	self.res     = res
	self.datatype = datatype
	self.time_period = time_period
        
	QtCore.QThread.__init__(self)
 

    def __del__(self):
        self.wait()

    def log(self, text):
        self.emit( QtCore.SIGNAL('update(QString)'), text )
 
    def run(self):
	self.log(" ")
	self.log("Downloading...")
	C = downloader.get(self.datatype)
	d = C(self.mindate, self.maxdate, self.res, self.time_period)
	self.tifs = d.download(self.path)
	if len(self.tifs[1]) > 0:
	    for f in self.tifs[1]:
	        self.log("Failed: {}".format(f))
	self.log("Complete.".format(self.path))



class OceanDataDialog(QtGui.QDialog, Ui_OceanData):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
	self.iface = iface

	self.data_desc = {
		'AQUA MODIS Chlorophyll Concentration': 'Mapped CHL-a concentrations \nValid date range: 2002/07/04 - present',
		'SeaWiFS Chlorophyll Concentration': 'Mapped CHL-a concentrations \nValid date range: 1997/09/04 - 2010/12/11',
		' ': '',
		'AQUA MODIS Sea Surface Temperature': 'Sea Surface Temperatures \nNot working yet.',
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
	self.btnDownload.setEnabled(False)
        mindate  = self.startDate.date()
        maxdate  = self.endDate.date()
        path     = self.txtPath.text()
        res      = self.comboBoxRes.currentText()
	res      = int(res.replace('km', ''))
	datatype = self.comboBoxDatasets.currentText()
	self.style = style_pick.get(datatype)
	period   = self.comboBoxTime.currentText()
	
	if path == "":
	    self.plainTextEdit.appendPlainText("Error: Enter a download directory.")
	    self.btnDownload.setEnabled(True)
	else:
            self.downloadThread = DownloadThread(path, mindate, maxdate, res, period, datatype)
            self.connect(self.downloadThread, QtCore.SIGNAL("update(QString)"), self.log)
            self.downloadThread.start()
	    self.connect(self.downloadThread, QtCore.SIGNAL('finished()'), self.addlayers)


    def addlayers(self):
	self.btnDownload.setEnabled(True)

        if self.checkBoxCanvas.isChecked() == True and hasattr(self.downloadThread, 'tifs'):
	    tifs = self.downloadThread.tifs[0]
	    if len(tifs) > 0:

                for t in tifs:
                    self.iface.addRasterLayer(t)
	    
	        layers = self.iface.legendInterface().layers()
	        pth = os.path.dirname(tifs[0])
	        qml = style_pick.makeqml(pth, self.style)

	        for l in layers:
		    l.loadNamedStyle(qml)
		    self.iface.legendInterface().refreshLayerSymbology(l)
	
	    os.remove(qml)

