from nasa_oceancolor.sst import Sst
from nasa_oceancolor.chl import Chl
from nasa_oceancolor.chlsw import Chlsw


__downloaders = {
	'sst': Sst,
	'AQUA MODIS Chlorophyll Concentration': Chl,
	'SeaWiFS Chlorophyll Concentration': Chlsw
}

def get(k):
	return __downloaders[k]


