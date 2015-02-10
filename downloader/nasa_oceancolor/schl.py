from datetime import datetime
from osgeo import gdal
from osgeo import osr
import numpy as np
from processor import Processor
import os


class Schl:
	"""
	Deals with download and geotif output of SeaWifs CHL-a concentration
	"""

	def __init__(self, start_date, end_date, res, time_composite='Annual'):
		
		self.start_date     = start_date
		self.end_date       = end_date
		self.res            = res
		self.time_composite = time_composite

                self.fns = {'fn_annual': 'S{0}001{0}{1}.L3m_YR_CHL_chlor_a_{2}km',
                                'fn_monthly': 'S{0}{1}{0}{2}.L3m_MO_CHL_chlor_a_{3}km',
                                'fn_8day': 'S{0}{1:0>3}{0}{2:0>3}.L3m_8D_CHL_chlor_a_{3}km',
                                'fn_daily': 'S{0}{1}.L3m_DAY_CHL_chlor_a_{2}km',
                                }
	
		self.P = Processor(start_date, end_date, res, time_composite, self.fns)

		if self.res == 4:
			self.geo = [-180.0, 0.04166666791, 0.0, 90.0, 0.0, -0.04166666791]
		elif self.res == 9:
			self.geo = [-180.0, 0.08333333582, 0.0, 90.0, 0.0, -0.08333333582]

    		self.outproj = osr.SpatialReference()
    		self.outproj.SetWellKnownGeogCS("WGS84")    
    		self.nodata = -32767


	def download(self, path):
		"""
		Input: path to download files to. 
		Other inputs are handled when creating class

		Downloads relevant HDFs and converts to geotiff.
	
		"""
		self.path = os.path.abspath(path)
		filenames = self.P.createfilenames()
		tiffiles = [[],[]]

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
		Converts HDF to GEOTIFF.
		Input: .hdf file

		Inserts metadata tags to output geotiff
		
		"""
		outname = '{0}.tif'.format(targetfile)
		g = gdal.Open(targetfile)
		
		arr = g.ReadAsArray()
		arr = np.array(arr)
		[cols, rows] = arr.shape
		
		outdata = gdal.GetDriverByName("GTiff")
		
		dst_ds = outdata.Create(outname, rows, cols, 1, gdal.GDT_Float32)
		
		band = dst_ds.GetRasterBand(1)
		band.SetNoDataValue(self.nodata)
		dst_ds.SetGeoTransform(self.geo)
		dst_ds.SetProjection(self.outproj.ExportToWkt())
		dst_ds.SetMetadataItem('SENSOR', 'SeaWiFS')
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
		dst_ds.SetMetadataItem('DATA START YEAR', g.GetMetadataItem('Period Start Year'))
		dst_ds.SetMetadataItem('DATA END YEAR', g.GetMetadataItem('Period End Year'))
		dst_ds.SetMetadataItem('PARAMETER', g.GetMetadataItem('Parameter'))
		dst_ds.SetMetadataItem('UNITS', g.GetMetadataItem('Units'))
		dst_ds.SetMetadataItem('NODATA VALUE', '{}'.format(self.nodata))
		dst_ds.SetMetadataItem('YEAR', g.GetMetadataItem('Start Year'))
		band.WriteArray(arr)

		g = None

		os.remove(targetfile)
		return outname

