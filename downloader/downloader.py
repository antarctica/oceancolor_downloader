from nasa_oceancolor.sst import Sst
from nasa_oceancolor.chl import Chl


__downloaders = {
	'sst': Sst,
	'AQUA MODIS Chlorophyll Concentration': Chl,
}

def get(k):
	return __downloaders[k]


