from nasa_oceancolor.sst import Sst
from nasa_oceancolor.chl import Chl


__downloaders = {
	'sst': Sst,
	'chl': Chl,
}

def get(k):
	return __downloaders[k]


