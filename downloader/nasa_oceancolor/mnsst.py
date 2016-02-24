from datetime import datetime
from osgeo import gdal
from osgeo import osr
import numpy as np
import os
from processor import Processor


class Mnsst():
    """
    Deals with download and geotiff output of AQUA MODIS NSST

    """

    def __init__(self, start_date, end_date, res, time_composite='Annual'):
            
        self.start_date     = start_date
        self.end_date       = end_date
        self.res            = res
        self.time_composite = time_composite

        self.fns = {'fn_annual': 'A{0}001{0}{1}.L3m_YR_NSST_sst_{2}km',
                        'fn_monthly': 'A{0}{1}{0}{2}.L3m_MO_NSST_sst_{3}km',
                        'fn_8day': 'A{0}{1:0>3}{0}{2:0>3}.L3m_8D_NSST_sst_{3}km',
                        'fn_daily': 'A{0}{1}.L3m_DAY_NSST_sst_{2}km',
                        }


        self.P = Processor(start_date, end_date, res, time_composite, self.fns) 

        if self.res == 4:
            self.geo = [-180.0, 0.04166666791, 0.0, 90.0, 0.0, -0.04166666791]
        elif self.res == 9:
            self.geo = [-180.0, 0.08333333582, 0.0, 90.0, 0.0, -0.08333333582]

        self.outproj = osr.SpatialReference()
        self.outproj.SetWellKnownGeogCS("WGS84")    
        self.nodata = 65535

    def setLogger(self, loggerObject):
        """
            Input: Class with .log function
            
            Logs message to this class.
    
        """
        self.P.setLogger(loggerObject)



    def download(self, path):
        """
        Input: path to download files to.
        
        Downloads relevant NETCDFs and converts to geotiff

        """
        self.path = os.path.abspath(path)
        filenames = self.P.createfilenames()
        tiffiles = [[],[]]

        self.P.file_no = 1
        for f in filenames:
            f = os.path.join(self.path, f)
            f_uncompress = self.P.extract(f)
            if not f_uncompress == 1:
                tif = self.__process(f_uncompress)
                tiffiles[0].append(tif)
                self.P.file_no += 1
            else:
                tiffiles[1].append(os.path.basename(f))
                self.P.file_no += 1
            
        return tiffiles



    def __process(self, targetfile):
        """
        Converts NC to GEOTIFFs. 
        Input: .nc file

        Inserts metadata tags to output geotiff

        """
        slope = 0.000717184972018003
        inter = -2
        
        self.P.log(targetfile)
        outname = '{0}.tif'.format(targetfile.replace('.nc', ''))

        g    = gdal.Open(targetfile)
        sub  = g.GetSubDatasets()
        #sst  = gdal.Open(sub[0][0])
        #qual = gdal.Open(sub[1][0])
        
        for s in sub:
            for s1 in s:
                if ':sst' in s1 or '://sst' in s1:
                    sst = gdal.Open(s1)
                if ':qual_sst' in s1 or '://qual_sst' in s1:
                    qual = gdal.Open(s1)

        sstarr  = sst.ReadAsArray()
        qualarr = qual.ReadAsArray()
        sstarr = np.array(sstarr, dtype=np.float32)
        qualarr = np.array(qualarr)

        [cols, rows] = sstarr.shape


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
        date = datetime.now()
        date = date.strftime('%Y-%m-%d')
        dst_ds.SetMetadataItem('DOWNLOAD_DATE', date)
        dst_ds.SetMetadataItem('DOWNLOAD_FROM', 'NASA OCEANCOLOR')
        dst_ds.SetMetadataItem('NODATA VALUE', '{}'.format(self.nodata))
        band.WriteArray(scaled)
        
        outdataqual = gdal.GetDriverByName("GTiff")
        dst_ds = outdataqual.Create(outname.replace('.tif', '_qual.tif'), rows, cols, 1, gdal.GDT_Byte)
        band = dst_ds.GetRasterBand(1)
        dst_ds.SetGeoTransform(self.geo)
        dst_ds.SetProjection(self.outproj.ExportToWkt())
        band.WriteArray(qualarr)

        g    = None
        sub  = None
        sst  = None
        qual = None
        
        os.remove(targetfile)
        return outname

