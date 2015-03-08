'''
Created on 6. juli 2012

@author: Joakim
'''
import webapp2
from ..Framework.Handler import Handler
from ..utils import url
from ..utils import smartEscape
from ..database.Wikipage import Wikipage

class wikimain(Handler):
    def get(self):
        self.write("Mainpage!")
        
class WikiPage(Handler):
    def get(self, pageName):
        v = self.request.get('v')
        if v.isdigit():
            pageName = pageName[:-1]
        page = Wikipage.getPage(pageName ,v)
        if not page and self.user:
            self.redirect(url.url['wikiedit']+pageName)
        elif not page and not self.user:
            self.redirect(url.url['wiki'])
        else:
            content = smartEscape.smartEscape(page.content)
            self.render("wikiShowPage.html", page=pageName, content=content)

class editPage(Handler):
    def get(self, pageName):
        if self.user:
            v = self.request.get('v')
            if v.isdigit():
                pageName = pageName[:-1]
            page = Wikipage.getPage(pageName,v)
            if page:
                content = page.content
            else:
                content = ''
            self.render("wikiEditPage.html", page=pageName, content=content)
        else:
            self.redirect(url.url['login'])
    def post(self, pageName):
        if self.user:
            content = self.request.get('content')
            w = Wikipage.update(content, pageName)
            w.put()
            
            self.redirect(url.url['wiki']+pageName)
        else:
            self.redirect(url.url['login'])

class history(Handler):
    def formatHistory(self, content, created):
        pass
    
    def get(self,pageName):
        history = Wikipage.getHistory(pageName)
        self.render('wikihistory.html', history=history, pageName=pageName)

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
app = webapp2.WSGIApplication([(url.url['wiki']+r'/?', wikimain),
                               (url.url['wikiedit']+PAGE_RE, editPage),
                               (url.url['wikihistory']+PAGE_RE, history),
                               (url.url['wiki']+PAGE_RE, WikiPage),
                               ],
                              debug=True)