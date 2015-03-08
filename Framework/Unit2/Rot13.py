'''
Created on 18. juni 2012

@author: Joakim
'''
import webapp2
import cgi

from ..utils import url
from ..Framework import framework

letters="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
lettersLower = "abcdefghijklmnopqrstuvwxyz"
lettersUpper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
inputFromUser = ""
form = """ 
<h1>ROT13 some Text!</h1>
<form method="post">
    <textarea name="text" rows="6" cols="50">%s</textarea>

    <br>
    <input type="submit">
</form>
"""
class MainPage(framework.Handler):
    def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        self.write(form %inputFromUser)
    def post(self):
        inputFromUser = cgi.escape(rot13(self.request.get('text')), quote=True)
        self.response.out.write(form%inputFromUser)
app = webapp2.WSGIApplication([(url.url['rot13']+r'/?', MainPage)],
                              debug=True)

def rot13(s):
    out = []
    for c in s:
        index = letters.find(c)
        if index > -1:
            if c.islower():
                c = lettersLower[(index+13)%len(lettersLower)]
            elif c.isupper():
                c = lettersUpper[(index+13)%len(lettersUpper)]                
        out.append(c)
    return ''.join(out)