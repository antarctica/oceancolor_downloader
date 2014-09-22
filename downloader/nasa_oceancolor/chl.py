from datetime import datetime
import osr

class Chl:
	"""
	This is my CHL class
	"""

	def __init__(self, start_date, end_date, res, time_composite='Annual'):
		
		#self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
		#self.end_date   = datetime.strptime(end_date, '%Y-%m-%d')

		self.start_yr       = start_date.year
		self.end_yr         = end_date.year
		self.res            = res
		self.time_composite = time_composite

		if self.res == 4:
			self.geo = [-180.0, 0.04166666791, 0.0, 90.0, 0.0, -0.04166666791]
		elif self.res == 9:
			self.geo = [-180.0, 0.08333333582, 0.0, 90.0, 0.0, -0.08333333582]

    		self.outproj = osr.SpatialReference()
    		self.outproj.SetWellKnownGeogCS("WGS84")    
    		self.nodata = -32767


	def __createfilenames(self):
		"""
		Creates a list of filenames based on inputs 
		"""
		valid_year_min = 2002
		valid_year_max = 2013

		#minyear = self.start_date.year
		#maxyear = self.end_date.year


		leap_years = [x for x in range(self.start_yr, self.end_yr+1) 
				if (x % 400 == 0) or (x % 4 == 0 and not x % 100 == 0)]

		filenames = []
		for year in range(self.start_yr, self.end_yr + 1):
			if year in leap_years:
				filenames.append('A{0}001{0}366.L3m_YR_CHL_chlor_a_{1}km'.format(year, self.res))
			else:
				filenames.append('A{0}001{0}365.L3m_YR_CHL_chlor_a_{1}km'.format(year, res))
		return filenames
	



	def download(self, path):
		"""
		This downlaods
	
		"""
		filenames = self.__createfilenames()
		return filenames



	def __process(self):
		"""
		This processes
		"""
		pass

	




