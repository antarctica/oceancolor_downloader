path_to_ftp = 'http://oceandata.sci.gsfc.nasa.gov/MODISA/Mapped/Annual/4km/chlor/'

f = 'http://oceandata.sci.gsfc.nasa.gov/cgi/getfile/A20020012002365.L3m_YR_CHL_chlor_a_4km.bz2'

import urllib
import bz2
import gdal

urllib.urlretrieve(f, 'test6.bz2')
uncom = bz2.BZ2File('test6.bz2', 'r').read()
output = open('test6', 'w')

output.write(uncom)

output.close()
g = gdal.Open('test6')
arr = g.ReadAsArray()

print arr


'''
NEXT
* Make into a function - this one downloads and converts a given file as input
* Work out the geotransform
* Save out as Geotif

* Make a new function which selects the file to download based on date
* Extend this to do a date range
'''
