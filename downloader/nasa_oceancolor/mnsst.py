from datetime import datetime
from osgeo import gdal
from osgeo import osr
import numpy as np
import os
from processor import Processor


class Mnsst():

	def __init__(self, start_date, end_date, res, time_composite='Annual'):
		
		self.start_date     = start_date
		self.end_date       = end_date
		self.res            = res
		self.time_composite = time_composite

		self.fns = {'fn_annual': 'A{0}001{0}366.L3m_YR_NSST_{1}',
				'fn_monthly': 'A{0}{1}{0}{2}.L3m_MO_NSST_{3}',
				'fn_8day': 'A{0}{1:0>3}{0}{2:0>3}.L3m_8D_NSST_{3}',
				'fn_daily': 'A{0}{1}.L3m_DAY_NSST_{2}',
				}


		self.P = Processor(start_date, end_date, res, time_composite, self.fns) 

		if self.res == 4:
			self.geo = [-180.0, 0.04166666791, 0.0, 90.0, 0.0, -0.04166666791]
		elif self.res == 9:
			self.geo = [-180.0, 0.08333333582, 0.0, 90.0, 0.0, -0.08333333582]

    		self.outproj = osr.SpatialReference()
    		self.outproj.SetWellKnownGeogCS("WGS84")    
    		self.nodata = 65535


	def download(self, path):
		"""
		This downloads
	
		"""
		self.path = os.path.abspath(path)
		filenames = self.P.createfilenames()
		tiffiles = [[],[]]

		# return [[tiffiles][failedfiles]]
		for f in filenames:
			f = os.path.join(self.path, f)
			f_uncompress = self.P.extract(f)
			if not f_uncompress == 1:
				tif = self.__process(f_uncompress)
				tiffiles[0].append(tif)
			else:
				tiffiles[1].append(os.path.basename(f))
		
		return tiffiles



	def __process(self, targetfile):
		"""
		This processes the uncompressed file downloaded 
		in self.__extract()
		"""
		outname = '{0}.tif'.format(targetfile)
		g    = gdal.Open(targetfile)
		sub  = g.GetSubDatasets()
		sst  = gdal.Open(sub[0][0])
		qual = gdal.Open(sub[1][0])
		
		sstarr  = sst.ReadAsArray()
		qualarr = qual.ReadAsArray()
		sstarr = np.array(sstarr, dtype=np.float32)
		qualarr = np.array(qualarr)

		[cols, rows] = sstarr.shape

		#scaling
		slope = float(sst.GetMetadataItem('Slope'))
		inter = float(sst.GetMetadataItem('Intercept'))

		m = np.ma.masked_values(sstarr, self.nodata)
		
		scaled = m * slope + inter

		outdata = gdal.GetDriverByName("GTiff")
		
		dst_ds = outdata.Create(outname, rows, cols, 1, gdal.GDT_Float32)
		
		band = dst_ds.GetRasterBand(1)
		band.SetNoDataValue(self.nodata)
		dst_ds.SetGeoTransform(self.geo)
		dst_ds.SetProjection(self.outproj.ExportToWkt())
		dst_ds.SetMetadataItem('SENSOR', 'AQUA_MODIS')
		dst_ds.SetMetadataItem('RESOLUTION', '{}km'.format(self.res))
		dst_ds.SetMetadataItem('DATA START DAY', g.GetMetadataItem('Period Start Day'))
		dst_ds.SetMetadataItem('DATA END DAY', g.GetMetadataItem('Period End Day'))
		dst_ds.SetMetadataItem('DATA START YEAR', g.GetMetadataItem('Period Start Year'))
		dst_ds.SetMetadataItem('DATA END YEAR', g.GetMetadataItem('Period End Year'))
		date = datetime.now()
		date = date.strftime('%Y-%m-%d')
		dst_ds.SetMetadataItem('DOWNLOAD_DATE', date)
		dst_ds.SetMetadataItem('DOWNLOAD_FROM', 'NASA OCEANCOLOUR')
		dst_ds.SetMetadataItem('PROCESSING_TIME',g.GetMetadataItem('Processing Time'))
		dst_ds.SetMetadataItem('PROCESSING_VERSION',g.GetMetadataItem('Processing Version'))
		dst_ds.SetMetadataItem('PARAMETER', g.GetMetadataItem('Parameter'))
		dst_ds.SetMetadataItem('UNITS', g.GetMetadataItem('Units'))
		dst_ds.SetMetadataItem('NODATA VALUE', '{}'.format(self.nodata))
		dst_ds.SetMetadataItem('YEAR', g.GetMetadataItem('Start Year'))
		band.WriteArray(scaled)
		
		outdataqual = gdal.GetDriverByName("GTiff")
		dst_ds = outdataqual.Create(outname.replace('.tif', '_qual.tif'), rows, cols, 1, gdal.GDT_Byte)
		band = dst_ds.GetRasterBand(1)
		dst_ds.SetGeoTransform(self.geo)
		dst_ds.SetProjection(self.outproj.ExportToWkt())
		band.WriteArray(qualarr)
		
		return outname


if __name__ == "__main__":
	sd = datetime(2003, 12, 15)
	ed = datetime(2003, 12, 30)
	d = Mnsst(sd, ed, 9, 'Annual')
	x = d.download('/Users/Ireland/rsr/qgis-dev/ref/')
	print x
