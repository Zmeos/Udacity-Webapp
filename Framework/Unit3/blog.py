'''
Created on 24. juni 2012

@author: Joakim
'''
import webapp2
import json

from ..utils.finalVars import finalVars
from ..Framework.Handler import Handler
from ..database.Blogpost import Blogpost
from ..utils import url


def postToDict(post): #json related
    createdDate = post.created.strftime("%a %b %d %H:%M:%S %y")
    return {"content":post.content, "subject":post.subject, "created":createdDate}

class MainPage(Handler):
    def get(self):
        self.render("test.html")
        
class NewPost(Handler):
    def render_newpost(self, subject="", content="", error=""):
        self.render("newpost.html", error = error, subject = subject, content=content)
    
    def get(self):
        if self.user:
            self.render_newpost()
        else:
            self.redirect(url.url['login'])
            
    def post(self):
        if self.user:
            subject = self.request.get("subject")
            content = self.request.get("content")
        
            if subject and content:
                b = Blogpost.register(subject, content, self.user)
                b.put()
                Blogpost.getBlogposts(finalVars.mc_blogkey,update=True)
                post_id = b.key().id()
                self.redirect(url.url['blog']+("/%s-%s"%(post_id,self.user.key().id())))

            else:
                error = "we need both Subject and Content!"
                self.render_newpost(error = error, subject = subject, content=content)
        else:
            self.redirect(url.url['login'])
class Blog(Handler):
    def render_blog(self):
        mc_key = finalVars.mc_blogkey
        blogposts, timeSinceQ = Blogpost.getBlogposts(mc_key)
        
        
        self.render("blog.html", blogposts=blogposts, timeSinceQ=timeSinceQ)
    def get(self):
        self.render_blog()
        
class PostHandler(Handler):
    def get(self, blog_id, user_id):
        post,timeSinceQ = Blogpost.getBlogposts(blog_id, user_id)
        if post:
            self.render("blogpost.html", post = post, timeSinceQ=timeSinceQ)
        else:
            self.write("<h1>This post does not exist!</h1>")

class PostJson(Handler):
    def get(self, blog_id):
        self.response.headers['Content-Type'] = 'application/json'
        post, timeSinceQ = Blogpost.getBlogposts(blog_id)
        if post:
            post = postToDict(post)
            permalink = {'post':post, 'timeSinceQuery':timeSinceQ}
            j = json.dumps(permalink)
            self.write(j)
    
    # dict with content, subject, created, last-modified

class BlogJson(Handler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        mc_key = finalVars.mc_blogkey
        blogposts, timeSinceQ = Blogpost.getBlogposts(mc_key)
        posts = [postToDict(post) for post in blogposts]
        front = {'posts':posts,'timeSinceQuery':timeSinceQ}
        j = json.dumps(front)
        self.write(j)
    #list with dict like in PostJson

class FlushCache(Handler):
    def get(self):
        Blogpost.flushCache()
        self.redirect(url.url['blog'])

app = webapp2.WSGIApplication([
                               webapp2.Route('/', handler=Blog, name='blog'), #just a test of the route function
                               (url.url['newpost']+r'/?', NewPost),
                               (url.url['blog']+r'/?', Blog),
                               (url.url['blog']+r'/(\d+)-(\d+)/?', PostHandler),
                               (url.url['blog']+r'/?.json', BlogJson),
                               (url.url['blog']+r'/(\d+)/?.json', PostJson),
                               (url.url['flush']+r'/?', FlushCache)],
                              debug=True)
