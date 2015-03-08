'''
Created on 18. juni 2012

@author: Joakim
'''


import webapp2
import re
import cgi

form = """<h1>Signup</h1>
<form method="POST">
    <div><label>Username<input type="text" name="username" value="%(username)s"></label>        <label style="color: red">%(usernameError)s</label>        </div>
    <div><label>Password<input type="password" name="password" value="%(password)s"></label>        <label style="color: red">%(passwordError)s</label>        </div>
    <div><label>Verify Password<input type="password" name="verify"value="%(verify)s"></label>      <label style="color: red">%(verifyError)s</label>            </div>
    <div><label>Email(optional)<input type="text" name="email"value="%(email)s"></label>        <label style="color: red">%(emailError)s</label>            </div>
    <input type="submit">
</form>"""


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_username(username):
    return USER_RE.match(username)

def valid_password(password):
    return PASS_RE.match(password)

def valid_email(email):
    return EMAIL_RE.match(email)

def escape(s):
    return cgi.escape(s, quote=True)


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, signup World!')

class BaseHandler(webapp2.RequestHandler):
    #def render(self, template, **kw):
    #    self.response.out.write(render_str(template,**kw))
    
    def write(self, *a, **kw):
        self.response.out.write(*a,**kw)
        
class Signup(BaseHandler):
    def write_form(self, username="", password="", verify="", email="", usernameError="", passwordError="", verifyError="", emailError=""):
        self.response.out.write(form % {"username":username,"password":password,"verify":verify,"email":email,"usernameError":usernameError,"passwordError":passwordError,"verifyError":verifyError,"emailError":emailError})
    def get(self):
        self.write_form()
    def post(self):
        usernameError = ""
        passwordError = ""
        verifyError = ""
        emailError = ""
        
        username = escape(self.request.get('username'))
        password = escape(self.request.get('password'))
        verify = escape(self.request.get('verify'))
        email = escape(self.request.get('email'))
        
        if not valid_username(username):
            usernameError = "Not a valid Username"
        if not valid_password(password):
            passwordError = "Not a valid Password"
            
        if not(password == verify):
            verifyError = "Does not match what you entered in the password field"
            
        if not valid_email(email) and email:
            emailError = "Not a valid Email"
        
        if (valid_email(email) or not email) and valid_password(password) and valid_username(username) and password==verify:
            self.redirect('/unit2/welcome/?username=%s'%username)
        
        self.write_form(username,password,verify,email,usernameError,passwordError,verifyError,emailError)
class Welcome(BaseHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.write('<h1>Welcome %s!</h1>'%(username))
        else:
            self.redirect('/unit2/signup')
app = webapp2.WSGIApplication([('/', MainPage),('/unit2/signup/?', Signup),('/unit2/welcome/?', Welcome)],
                              debug=True)
