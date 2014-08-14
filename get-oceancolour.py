f = 'http://oceandata.sci.gsfc.nasa.gov/cgi/getfile/A20020012002365.L3m_YR_CHL_chlor_a_4km.bz2'

workingdir = '/Users/Ireland/rsr/qgis-dev/'

import urllib
import bz2
import gdal
import osr

def getdata(filenames):
  '''
  Takes the filename which has been generated in 
  createfilename() and downloads and creates a GeoTiff
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


def getfilenames(minyear, maxyear):
  '''
  Input year 'from' and 'to' that you you want annual grids for.
  Returns a list of filenames.
  '''

  filenames = []
  for year in range(minyear, maxyear+1):
    print year
    #MODIS AQUA chl-a Annual 4km
    filenames.append('A{0}001{0}365.L3m_YR_CHL_chlor_a_4km'.format(year))

  return filenames
  

if __name__ == '__main__':
  
  files = getfilenames(2002, 2004)
  getdata(files)

