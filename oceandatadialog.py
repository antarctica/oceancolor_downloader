# -*- coding: utf-8 -*-
"""
/***************************************************************************
 OceanDataDialog
                                 A QGIS plugin
                             -------------------
        begin                : 2014-08-13
        copyright            : (C) 2015 by NERC BAS
        email                : basmagic@bas.ac.uk
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


class DownloadThread(QtCore.QThread):
    def __init__(self, path, mindate, maxdate, res, time_period, datatype):
        self.path    = os.path.abspath(path)
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
	if self.mindate > self.maxdate:
            self.log("Error: Invalid date range.\n")
        else:
	    self.log("Downloading...")
	    C = downloader.get(self.datatype)
	    d = C(self.mindate, self.maxdate, self.res, self.time_period)
            d.setLogger(self)
	    self.tifs = d.download(self.path)
	    if len(self.tifs[1]) > 0:
	        for f in self.tifs[1]:
	            self.log("\nUnable to download file: {}. Does not exist\n".format(f))
	    self.log("Complete.".format(self.path))



class OceanDataDialog(QtGui.QDialog, Ui_OceanData):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
	self.iface = iface

	self.data_desc = {
		'AQUA MODIS Chlorophyll Concentration': 'Mapped CHL-a concentrations \nValid date range: 2002/07/04 - present\n',
		'SeaWiFS Chlorophyll Concentration': 'Mapped CHL-a concentrations \nValid date range: 1997/09/04 - 2010/12/11\n',
		' ': '\n',
		'AQUA MODIS Sea Surface Temperature': 'Mapped Night Sea Surface Temperatures \nValid date range: 2002/07/04 - present\n',
	}

    
    def log(self, text):
        self.plainTextEdit.appendPlainText(text)

    def update(self):
	if not self.comboBoxDatasets.currentText() == ' ':
	    self.btnDownload.setEnabled(True)
	else:
            self.btnDownload.setEnabled(False)

	self.plainTextEdit.clear()
        data_type = self.data_desc[self.comboBoxDatasets.currentText()]
	self.plainTextEdit.appendPlainText('For full details of source datasets, refer to http://oceancolor.gsfc.nasa.gov/\n')
	self.plainTextEdit.appendPlainText(data_type)
	
	self.comboBoxRes.clear()

	mindate_sc = QtCore.QDate()
	mindate_sc.setDate(1997,9,4)
	maxdate_sc = QtCore.QDate()
	maxdate_sc.setDate(2010,12,11)
	
	mindate_mc = QtCore.QDate()
        mindate_mc.setDate(2002,7,4)
	maxdate_mc = QtCore.QDate()
	maxdate_mc = maxdate_mc.currentDate()

	if self.comboBoxDatasets.currentText() == 'SeaWiFS Chlorophyll Concentration':
	    self.comboBoxRes.insertItem(0, '9km')
	    self.startDate.setDate(mindate_sc)
	    self.startDate.setDateRange(mindate_sc, maxdate_sc)
	    self.endDate.setDate(maxdate_sc)
	    self.endDate.setDateRange(mindate_sc, maxdate_sc)

	if self.comboBoxDatasets.currentText() == 'AQUA MODIS Chlorophyll Concentration':
	    self.comboBoxRes.insertItems(0, ['9km', '4km'])
	    self.startDate.setDate(mindate_mc)
	    self.startDate.setDateRange(mindate_mc, maxdate_mc)
	    self.endDate.setDate(maxdate_mc)
	    self.endDate.setDateRange(mindate_mc, maxdate_mc)

	if self.comboBoxDatasets.currentText() == 'AQUA MODIS Sea Surface Temperature':
	    self.comboBoxRes.insertItems(0, ['9km', '4km'])
	    self.startDate.setDate(mindate_mc)
	    self.startDate.setDateRange(mindate_mc, maxdate_mc)
	    self.endDate.setDate(maxdate_mc)
	    self.endDate.setDateRange(mindate_mc, maxdate_mc)


    def open(self):
	self.fileDialog = QtGui.QFileDialog(self)
	#self.fileDialog.show()
	self.txtPath.setText(self.fileDialog.getExistingDirectory())

    def accept(self):
	self.btnDownload.setEnabled(False)
        self.comboBoxDatasets.setEnabled(False)
        self.comboBoxTime.setEnabled(False)
	self.startDate.setEnabled(False)
	self.endDate.setEnabled(False)
	self.comboBoxRes.setEnabled(False)
	self.toolButton.setEnabled(False)

	mindate    = self.startDate.date()
        maxdate    = self.endDate.date()
        path       = self.txtPath.text()
        res        = self.comboBoxRes.currentText()
	res        = int(res.replace('km', ''))
	datatype   = self.comboBoxDatasets.currentText()
	self.style = style_pick.get(datatype)
	period     = self.comboBoxTime.currentText()
	
	if path == "":
	    self.plainTextEdit.appendPlainText("Error: Enter a download directory.")
	    self.btnDownload.setEnabled(True)
	    self.comboBoxDatasets.setEnabled(True)
            self.comboBoxTime.setEnabled(True)
	    self.startDate.setEnabled(True)
	    self.endDate.setEnabled(True)
	    self.comboBoxRes.setEnabled(True)
	    self.toolButton.setEnabled(True)
	else:
	    self.btnCancel.setEnabled(True)
	    self.btnClose.setEnabled(False)
            self.downloadThread = DownloadThread(path, mindate, maxdate, res, period, datatype)
            self.connect(self.downloadThread, QtCore.SIGNAL("update(QString)"), self.log)
            self.downloadThread.start()
	    self.connect(self.downloadThread, QtCore.SIGNAL('finished()'), self.addlayers)

    def stop(self):
	self.downloadThread.terminate()
	self.log('Download cancelled')
        self.btnCancel.setEnabled(False)
	self.btnClose.setEnabled(True)

    def addlayers(self):
	self.btnDownload.setEnabled(True)
	self.btnCancel.setEnabled(False)
	self.btnClose.setEnabled(True)
	self.comboBoxDatasets.setEnabled(True)
        self.comboBoxTime.setEnabled(True)
	self.startDate.setEnabled(True)
	self.endDate.setEnabled(True)
	self.comboBoxRes.setEnabled(True)
	self.toolButton.setEnabled(True)
        
	if self.checkBoxCanvas.isChecked() == True and hasattr(self.downloadThread, 'tifs'):
	    tifs = self.downloadThread.tifs[0]
	    if len(tifs) > 0:
                justnames = []
		for t in tifs:
                    self.iface.addRasterLayer(t)
		    n = os.path.basename(t).replace('.tif', '')
		    justnames.append(n)

	        layers = self.iface.legendInterface().layers()
	        pth = os.path.dirname(tifs[0])
	        qml = style_pick.makeqml(pth, self.style)

	        for l in layers:
	            if l.name() in justnames:
		        l.loadNamedStyle(qml)
		        self.iface.legendInterface().refreshLayerSymbology(l)
	
	        os.remove(qml)

