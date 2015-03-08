'''
Created on 1. juli 2012

@author: Joakim
'''

import logging

from ..utils import cookie
from google.appengine.ext import db
from google.appengine.api import memcache

def users_key(group='default'):
    #r = memcache.get()
    return db.Key.from_path('users', group)


class User(db.Model):
    name = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty()
    
    @classmethod
    def by_id(cls, uid):
        return cls.get_by_id(uid, parent = users_key())
    
    @classmethod
    def by_name(cls, name):
        #u = cls.all().filter('name =', name).get() #for some reason not working?? #should be working now
        u = db.GqlQuery("SELECT * FROM User WHERE name='%s'"%name)
        return u.get()
    @classmethod
    def register(cls, name, pw, email=None):
        pw_hash = cookie.make_pw_hash(name,pw)
        return cls(parent = users_key(),
                   name = name,
                   pw_hash = pw_hash,
                   email = email)
    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and cookie.valid_pw(name, pw,u.pw_hash):
            return u
