'''
Created on 9. juli 2012

@author: Joakim
'''
import cgi
#import logging

def smartEscape(s):
    s = cgi.escape(s, quote=True)
    #logging.error(s)
    s = s.replace("&lt;br&gt;", '<br>') # newline
    s = s.replace("&lt;b&gt;", '<b>').replace("&lt;/b&gt;", '</b>') # blod
    s = s.replace("&lt;h2&gt;", '<h2>').replace("&lt;/h2&gt;", '</h2>') # h2
    #logging.error(s)
    return s