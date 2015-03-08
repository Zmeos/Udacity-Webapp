'''
Created on 6. juli 2012

@author: Joakim
'''
from google.appengine.ext import db

class Wikipage(db.Model):
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    
    @classmethod
    def update(cls, content, page):
        key = db.Key.from_path('wiki', page)
        return cls(content=content, parent=key)
    
    @classmethod
    def getPage(cls, page, version):
        q = cls.all()
        key = db.Key.from_path('wiki', page)
        if q.ancestor(key) is None:
            return None
        list = q.ancestor(key).order('-created').fetch(20)
        if not list:
            return None
        if not version.isdigit():
            return list[0]
        version = int(version)
        return list[version-1]
    
    @classmethod
    def getHistory(cls, page):
        q = cls.all()
        key = db.Key.from_path('wiki', page)
        if q.ancestor(key) is None:
            return None
        return q.ancestor(key).order('-created').fetch(20)