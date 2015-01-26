#This one works!! Use this. Somehow use this to warn if something does not exist.
'''
import requests

#response = requests.get('http://oceandata.sci.gsfc.nasa.gov/cgi/getfile/{}.bz2'.format('S20072442007273.L3m_MO_CHL_chlor_a_9km'))
response = requests.get('http://oceandata.sci.gsfc.nasa.gov/cgi/getfile/{}.bz2'.format('S20080612008091.L3m_MO_CHL_chlor_a_9km'))
if response.status_code < 400:
	print 'ok'
else:
	print 'does not exist'
'''


import urllib2

try:
	f = urllib2.urlopen(urllib2.Request('http://oceandata.sci.gsfc.nasa.gov/cgi/getfile/{}.bz2'.format('S20080612008091.L3m_MO_CHL_chlor_a_9km')))
	deadLinkFound = False
except:
	deadLinkFound = True
	print 'no file'
