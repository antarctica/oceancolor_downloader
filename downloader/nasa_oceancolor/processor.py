from datetime import timedelta
from datetime import datetime
import os
import ocfiledates
from dateutil.relativedelta import relativedelta
import urllib2
import bz2

class Processor():
	"""
	Contains all processing functions general to all Oceancolor products. 
	"""

	def __init__(self, start_date, end_date, res, time_composite, filenames):
		self.start_date     = start_date
		self.end_date       = end_date
		self.res            = res
		self.time_composite = time_composite
		self.fns            = filenames
		self.logger         = None

	def log(self, message):
		"""
		Input: string message
		
		Logs message using logger object
	
		"""
		if(self.logger):
			self.logger.log(message)

	def setLogger(self, loggerObject):
		"""
		Input: Class with .log function
		
		Logs message to this class.
	
		"""
		self.logger = loggerObject
		self.log("* Processor loaded. Preparing to start download.")

	def chunk_read(self, output, response, chunk_size=8192*64):
		"""
		Method to download a file in chunks. Takes an output file, urllib2 response object and a 
		chunk size.
		"""

		total_size = response.info().getheader('Content-Length').strip()
		total_size = int(total_size)
		bytes_so_far = 0

		f = open(output, 'wb')
				
		while 1:
			chunk = response.read(chunk_size)
			bytes_so_far += len(chunk)

			if not chunk:
				break

			f.write(chunk)
			
			percent = float(bytes_so_far) / total_size
			percent = round(percent*100, 2)
		
			self.log("Downloaded %d of %d bytes (%0.2f%%)" % (bytes_so_far, total_size, percent))

		self.log(' ')
		
		f.close()

		return bytes_so_far

	def extract(self, targetfile):
		"""
		Method to download and extract a file
		"""
		self.log('* Downloading file {0} of {1}'.format(self.file_no, self.no_files))


		f_download = 'http://oceandata.sci.gsfc.nasa.gov/cgi/getfile/{}.bz2'.format(os.path.basename(targetfile))
		f_compress = '{}.bz2'.format(targetfile)
		f_uncompress = targetfile

		self.log("* Dataset: " + os.path.basename(targetfile))

		try:
			#thefile = urllib2.urlopen(f_download)
			#f = open(f_compress, 'wb')
			#f.write(thefile.read())
			#f.close()

			thefile = urllib2.urlopen(f_download)
			self.log("File size: " + str(thefile.info().getheader('Content-Length').strip()) )
			self.chunk_read(f_compress, thefile) # Instead of the open/write/close trio

			uncom = bz2.BZ2File(f_compress, 'rb').read()
			output = open(f_uncompress, 'wb')
			output.write(uncom)
			output.close()
			os.remove(f_compress)
			return f_uncompress

		except urllib2.URLError, e:    		
			self.log("URLError - could not download file\n")
			return 1
		



	def createfilenames(self):
		"""
		Creates a list of filenames based on inputs 
		"""
		minyear = self.start_date.year
		maxyear = self.end_date.year

		leap_years = [x for x in range(minyear, maxyear+1)
			if (x % 400 == 0) or (x % 4 == 0 and not x % 100 == 0)]

		filenames = []
		if self.time_composite == 'Annual':

			minyear = self.start_date.year
			maxyear = self.end_date.year

			for year in range(minyear, maxyear + 1):
				if year in leap_years:
					filenames.append(self.fns['fn_annual'].format(year, 366, self.res))
				else:
					filenames.append(self.fns['fn_annual'].format(year, 365, self.res))


		if self.time_composite == 'Monthly':
			d = self.start_date
			while d <= self.end_date:
				m = d.month
				if d.year in leap_years:
					date_ref = ocfiledates.monthly_leap
				else:
					date_ref = ocfiledates.monthly_nonleap
				filenames.append(self.fns['fn_monthly'].format(d.year, date_ref[m][0], date_ref[m][1], self.res))
				d = d + relativedelta(months=1)



		if self.time_composite == '8 day':
			d = self.start_date
			doy = d.strftime('%j')
			date_ref = ocfiledates.wk
			#get it so the date is at the start of any 8 day period to initialise the loop
			for dr in date_ref:
				if int(doy) in dr:
					doy = min(dr)
					d = datetime(d.year, 1, 1) + timedelta(doy - 1)
			while d <= self.end_date:
				doy = d.strftime('%j')
				if d.year in leap_years:
					date_ref = ocfiledates.wk_leap
					mindoy = int(doy)
					maxdoy = max(date_ref[mindoy])
					filenames.append(self.fns['fn_8day'].format(d.year, mindoy, maxdoy, self.res))
					if mindoy == 361:
						d = d + relativedelta(days=6)
					else:
						d = d + relativedelta(days=8)
				else:

					date_ref = ocfiledates.wk_nonleap
					mindoy = int(doy)
					maxdoy = max(date_ref[mindoy])
					filenames.append(self.fns['fn_8day'].format(d.year, mindoy, maxdoy, self.res))
					if mindoy == 361:
						d = d + relativedelta(days=5)
					else:
						d = d + relativedelta(days=8)


		if self.time_composite == 'Daily':
			d = self.start_date
			while d <= self.end_date:
				doy = d.strftime('%j')
				filenames.append(self.fns['fn_daily'].format(d.year, doy, self.res))
				d = d + relativedelta(days=1)


		self.no_files = len(filenames)
		self.log('* NUMBER OF FILES STAGED FOR DOWNLOAD: {}'.format(self.no_files))
		return filenames

