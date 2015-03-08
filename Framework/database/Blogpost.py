'''
Created on 1. juli 2012

@author: Joakim
'''

import os
import jinja2
import logging
import cgi



from datetime import datetime, timedelta
from google.appengine.ext import db
from google.appengine.api import memcache
from ..utils.finalVars import finalVars
from ..utils import url
from User import User

template_dir = os.path.join(os.path.split(os.path.dirname(__file__))[0], 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), 
                               autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    params['url'] = url.url
    return t.render(params)


class Blogpost(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    
    def render(self):
        self._render_text = cgi.escape(self.content,quote=True).replace('\n', '<br>')
        return render_str("post.html", post = self, user=self.parent())

    @classmethod
    def register(cls, subject, content, user):
        return cls(subject=subject, content=content, parent=user)
    
    @classmethod
    def getBlogposts(cls,key, author_id=0,update=False):#blogposts or blogpost
        posts, age = cls.age_get(key)
        if posts is None or update:
            logging.error('DB Query!')
            if key==finalVars.mc_blogkey: #check if blogfront
                query = db.GqlQuery("SELECT * FROM Blogpost ORDER BY created DESC LIMIT 10")
                posts = list(query)
            else: #must be permalink
                if int(author_id) != 0:
                    posts = Blogpost.get_by_id(int(key), parent=User.by_id(int(author_id)))
                else:
                    posts = Blogpost.get_by_id(int(key), parent=None)
                if posts is None:
                    logging.error("It seems like we found nothing! blogpost key:%s, and blogpost:%s"%(key,posts))
                    return None, 0 # if there is no such post we do not want to cache it   
            cls.age_set(key, posts)
        return posts, age
    
    @classmethod
    def age_set(cls, key, val):
        save_time = datetime.utcnow()
        memcache.set(key, (val,save_time))
    @classmethod
    def age_get(cls, key):
        r = memcache.get(key)
        if r:
            val,save_time = r
            age = (datetime.utcnow() - save_time).total_seconds()
        else:
            val , age = None, 0
        return val, age
    
    @classmethod
    def flushCache(cls):
        memcache.flush_all()

