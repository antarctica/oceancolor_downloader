path_to_ftp = 'http://oceandata.sci.gsfc.nasa.gov/MODISA/Mapped/Annual/4km/chlor/'

f = 'http://oceandata.sci.gsfc.nasa.gov/cgi/getfile/A20020012002365.L3m_YR_CHL_chlor_a_4km.bz2'

workingdir = '/Users/Ireland/rsr/qgis-dev/'

import urllib
import bz2
import gdal
import osr

def getdata(filename):
  '''
  Takes the filename which has been generated in 
  createfilename() and downloads and creates a GeoTiff
  '''

  nodata  = -32767
  
  outgeo  = [-180.0, 0.04166666791, 0.0, 90.0, 0.0, -0.04166666791]
  outproj = osr.SpatialReference()
  outproj.SetWellKnownGeogCS("WGS84")
  
  outname = '{0}{1}.tif'.format(workingdir, filename)


  f_download   = 'http://oceandata.sci.gsfc.nasa.gov/cgi/getfile/{}.bz2'.format(filename)
  f_compress   = '{0}{1}.bz2'.format(workingdir, filename)
  f_uncompress = '{0}{1}'.format(workingdir, filename)

  print 'downloading...'
  urllib.urlretrieve(f_download, f_compress)
  print 'uncompressing file...'
  uncom = bz2.BZ2File(f_compress, 'r').read()
  print ''
  output = open(f_uncompress, 'w')
  output.write(uncom)
  output.close()
  

  print 'creating geotif...'
  g = gdal.Open(f_uncompress)
  arr = g.ReadAsArray()
  [cols, rows] = arr.shape

  outdata = gdal.GetDriverByName("GTiff")
  dst_ds = outdata.Create(outname, rows, cols, 1, gdal.GDT_Float32)
  band = dst_ds.GetRasterBand(1)
  band.SetNoDataValue(nodata)
  dst_ds.SetGeoTransform(outgeo)
  dst_ds.SetProjection(outproj.ExportToWkt())
  band.WriteArray(arr)


'''
NEXT
* Make into a function - this one downloads and converts a given file as input
* Work out the geotransform
* Save out as Geotif

* Make a new function which selects the file to download based on date
* Extend this to do a date range
'''


if __name__ == '__main__':
  getdata('A20020012002365.L3m_YR_CHL_chlor_a_4km')
