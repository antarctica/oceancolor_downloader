from nasa_oceancolor.mnsst import Mnsst
from nasa_oceancolor.mchl import Mchl
from nasa_oceancolor.schl import Schl

"""
Selects which class to use to download data, based on UI input
"""

__downloaders = {
	'AQUA MODIS Sea Surface Temperature': Mnsst,
	'AQUA MODIS Chlorophyll Concentration': Mchl,
	'SeaWiFS Chlorophyll Concentration': Schl
}

def get(k):
	return __downloaders[k]


