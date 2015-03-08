'''
Created on 1. juli 2012

@author: Joakim
'''

import random
import string
import hashlib
import hmac

from finalVars import finalVars


def hash_str(s):
    return hmac.new(finalVars.hmacSECRET,s).hexdigest()

def make_secure_val(s): # s = val
    return "%s|%s" % (s, hash_str(s))

def check_secure_val(h): # h = secureval
    val = h.split('|')[0]
    if h == make_secure_val(val):
        return val


### More related to DB stuff, but whatever
def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

def make_pw_hash(name, pw):
    salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (h, salt)

def valid_pw(name, pw, h):
    hashSalt = h.split('|')
    hashPart = hashSalt[0]
    salt = hashSalt[1]
    
    if hashlib.sha256(name + pw + salt).hexdigest() == hashPart:
        return True
    return False
