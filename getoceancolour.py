
import urllib
import bz2
import gdal
import osr
import numpy as np
import datetime


def getdata(workingdir, filenames):
  '''
  Takes the filenames list which has been generated in 
  createfilename() and downloads and creates a GeoTiff
  from all of them.
  '''

  nodata  = -32767
  
  outgeo  = [-180.0, 0.04166666791, 0.0, 90.0, 0.0, -0.04166666791]
  outproj = osr.SpatialReference()
  outproj.SetWellKnownGeogCS("WGS84")
  
  for filename in filenames:
    outname = '{0}{1}.tif'.format(workingdir, filename)

    f_download   = 'http://oceandata.sci.gsfc.nasa.gov/cgi/getfile/{}.bz2'.format(filename)
    f_compress   = '{0}{1}.bz2'.format(workingdir, filename)
    f_uncompress = '{0}{1}'.format(workingdir, filename)

    print 'downloading...'
    urllib.urlretrieve(f_download, f_compress)
    print 'uncompressing file...'
    print f_compress
    uncom = bz2.BZ2File(f_compress, 'r').read()
    output = open(f_uncompress, 'w')
    output.write(uncom)
    output.close()

    print 'creating geotif...'
    g = gdal.Open(f_uncompress)
    arr = g.ReadAsArray()
    arr = np.array(arr)
    [cols, rows] = arr.shape

    outdata = gdal.GetDriverByName("GTiff")
    dst_ds = outdata.Create(outname, rows, cols, 1, gdal.GDT_Float32)
    band = dst_ds.GetRasterBand(1)
    band.SetNoDataValue(nodata)
    dst_ds.SetGeoTransform(outgeo)
    dst_ds.SetProjection(outproj.ExportToWkt())
    #set metadata tags
    dst_ds.SetMetadataItem('SENSOR', 'AQUA_MODIS')
    dst_ds.SetMetadataItem('RESOLUTION', '4km')
    date = datetime.datetime.now()
    date = date.strftime('%Y-%m-%d')
    dst_ds.SetMetadataItem('DOWNLOAD_DATE', date)
    dst_ds.SetMetadataItem('DOWNLOAD_FROM', 'NASA OCEANCOLOUR')
    dst_ds.SetMetadataItem('PRODUCT_NAME', filename)
    dst_ds.SetMetadataItem('UNITS', g.GetMetadataItem('Units'))
    #maybe to make more general, import start time and end time from input data instead,
    #so then would work with monthly and weekly...
    dst_ds.SetMetadataItem('YEAR', g.GetMetadataItem('Start Year'))
    band.WriteArray(arr)


def getfilenames(minyear, maxyear):
  '''
  Input year 'from' and 'to' that you you want annual grids for.
  Returns a list of filenames.
  '''
  validmin = 2002
  validmax = 2013  

  if minyear < validmin or maxyear > validmax:
    raise UserWarning('Input years out of range. Choose between 2002 and 2013')
 
  #leap years?
  leapyears = [x for x in xrange(minyear, maxyear + 1)
            if (x % 400 == 0) or (x % 4 == 0 and not x % 100 == 0)]

  filenames = []
  for year in range(minyear, maxyear+1):
    #MODIS AQUA chl-a Annual 4km
    if year in leapyears:
      filenames.append('A{0}001{0}366.L3m_YR_CHL_chlor_a_4km'.format(year))
    else:
      filenames.append('A{0}001{0}365.L3m_YR_CHL_chlor_a_4km'.format(year))

  return filenames
  

if __name__ == '__main__':
  
  files = getfilenames(2003, 2004)
  getdata(files)

