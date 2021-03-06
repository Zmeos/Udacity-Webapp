'''
Created on 1. juli 2012

@author: Joakim
'''

import os
import webapp2
import jinja2


from ..utils import cookie
from ..database.User import User
from ..utils import url

template_dir = os.path.join(os.path.split(os.path.dirname(__file__))[0], 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), 
                               autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a,**kw):
        self.response.out.write(*a,**kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        params['url'] = url.url
        params['user'] = self.user
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
    
    def set_secure_cookie(self, name, val):
        cookie_val = cookie.make_secure_val(val)
        self.response.headers.add_header(
                                         'Set-Cookie',
                                         '%s=%s; Path=/' % (name,cookie_val))
    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and cookie.check_secure_val(cookie_val)
    
    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))
        
    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
        
    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))
