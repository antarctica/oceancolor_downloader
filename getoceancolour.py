import urllib
import bz2
import gdal
import osr
import numpy as np
import datetime
import ocfiledates

class getoceancolour():

  def __init__(self):
    '''
    Using this to set standard parameters for the data conversion etc...
    '''
    self.geo4km = [-180.0, 0.04166666791, 0.0, 90.0, 0.0, -0.04166666791]
    self.geo9km = [-180.0, 0.08333333582, 0.0, 90.0, 0.0, -0.08333333582]
    self.outproj = osr.SpatialReference()
    self.outproj.SetWellKnownGeogCS("WGS84")    
    self.chlnodata = -32767

    self.monthlyint_nonleap = ocfiledates.monthly_nonleap
    self.monthlyint_leap    = ocfiledates.monthly_leap   
    

  #This is unfinished! Can't work out how to increment months
  #you can do a time delta by one month, within a while loop?
  #then you would need some test to work out if the date was older than the max date?! 
  def get_chl_monthly_filenames(self, mindate, maxdate, res):
    '''
    Returns a list of monthly filenames for CHL-a
    Input min/max year and month
    Matches to the monthly periods
    '''
    
    startdate = datetime.datetime.strptime(mindate, '%Y-%m-%d')
    enddate   = datetime.datetime.strptime(maxdate, '%Y-%m-%d')

    startyear  = int(startdate.strftime('%Y'))
    endyear    = int(enddate.strftime('%Y'))
    startmonth = int(startdate.strftime('%m'))
    endmonth   = int(enddate.strftime('%m'))

    print startyear, endyear, startmonth, endmonth

 

  def get_chl_annual_filenames(self, minyear, maxyear, res):
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
      #MODIS AQUA chl-a Annual 4km or 9km
      if year in leapyears:
        filenames.append('A{0}001{0}366.L3m_YR_CHL_chlor_a_{1}km'.format(year, res))
      else:
        filenames.append('A{0}001{0}365.L3m_YR_CHL_chlor_a_{1}km'.format(year, res))

    return filenames


  def get_chl_data(self, workingdir, filenames, res):
    '''
    Takes the filenames list which has been generated in 
    createfilename() and downloads and creates a GeoTiff
    from all of them.
    '''
     
    if res == 4:
      outgeo = self.geo4km
    if res == 9:
      outgeo = self.geo9km

    for filename in filenames:
      outname = '{0}{1}.tif'.format(workingdir, filename)

      f_download   = 'http://oceandata.sci.gsfc.nasa.gov/cgi/getfile/{}.bz2'.format(filename)
      f_compress   = '{0}{1}.bz2'.format(workingdir, filename)
      f_uncompress = '{0}{1}'.format(workingdir, filename)

      urllib.urlretrieve(f_download, f_compress)
      uncom = bz2.BZ2File(f_compress, 'r').read()
      output = open(f_uncompress, 'w')
      output.write(uncom)
      output.close()

      g = gdal.Open(f_uncompress)
      arr = g.ReadAsArray()
      arr = np.array(arr)
      [cols, rows] = arr.shape

      outdata = gdal.GetDriverByName("GTiff")
      dst_ds = outdata.Create(outname, rows, cols, 1, gdal.GDT_Float32)
      band = dst_ds.GetRasterBand(1)
      band.SetNoDataValue(self.chlnodata)
      dst_ds.SetGeoTransform(outgeo)
      dst_ds.SetProjection(self.outproj.ExportToWkt())
      #set metadata tags
      dst_ds.SetMetadataItem('SENSOR', 'AQUA_MODIS')
      dst_ds.SetMetadataItem('RESOLUTION', '{}km'.format(res))
      dst_ds.SetMetadataItem('DATA START DAY', g.GetMetadataItem('Period Start Day'))
      dst_ds.SetMetadataItem('DATA END DAY', g.GetMetadataItem('Period End Day'))
      dst_ds.SetMetadataItem('DATA START YEAR', g.GetMetadataItem('Period Start Year'))
      dst_ds.SetMetadataItem('DATA END YEAR', g.GetMetadataItem('Period End Year'))
      date = datetime.datetime.now()
      date = date.strftime('%Y-%m-%d')
      dst_ds.SetMetadataItem('DOWNLOAD_DATE', date)
      dst_ds.SetMetadataItem('DOWNLOAD_FROM', 'NASA OCEANCOLOUR')
      dst_ds.SetMetadataItem('PRODUCT_NAME', filename)
      dst_ds.SetMetadataItem('PARAMETER', g.GetMetadataItem('Parameter'))
      dst_ds.SetMetadataItem('UNITS', g.GetMetadataItem('Units'))
      dst_ds.SetMetadataItem('NODATA VALUE', '{}'.format(self.chlnodata))
      dst_ds.SetMetadataItem('YEAR', g.GetMetadataItem('Start Year'))
      band.WriteArray(arr)



if __name__ == '__main__':
 
  C = getoceancolour() 
  files = C.get_chl_monthly_filenames('2003-07-07', '2006-02-01', 4)
  #files = C.get_chl_annual_filenames(2006, 2006, 9)
  #C.get_chl_data('/Users/Ireland/rsr/qgis-dev/', files, 9)

