'''
Created on 29. juni 2012

@author: Joakim
'''

# QUIZ implement the basic memcache functions

CACHE = {}

#return True after setting the data
def set(key, value):
    if key not in CACHE:
        CACHE[key] = value
        return True
    ###Your set code here.

#return the value for key
def get(key):
    if key in CACHE:
        return CACHE[key]
    ###Your get code here.

#delete key from the cache
def delete(key):
    if key in CACHE:
        del CACHE[key]
    ###Your delete code here.

#clear the entire cache
def flush():
    CACHE.clear()
    ###Your flush code here.

#print set('x', 1)
#>>> True

#print get('x')
#>>> 1

#print get('y')
#>>> None

#delete('x')
#print get('x')
#>>> None