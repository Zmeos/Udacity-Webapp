'''
Created on 28. juni 2012

@author: Joakim
'''
import urllib2
from xml.dom import minidom

p  = urllib2.urlopen("http://www.nytimes.com/services/xml/rss/nyt/GlobalHome.xml")

c = p.read()

x = minidom.parseString(c)

print len(x.getElementsByTagName("item"))

#print minidom.parseString

#p.headers.items()
#for met in dir(p):
#    print met