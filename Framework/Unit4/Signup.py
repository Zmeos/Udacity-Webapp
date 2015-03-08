'''
Created on 18. juni 2012

@author: Joakim
'''

import webapp2

from ..utils import cookie
from ..utils import validCheck
from ..utils import url
from ..database.User import User
from ..Framework.Handler import Handler

   
class Signup(Handler):
    def write_form(self, username="", password="", verify="", email="", usernameError="", passwordError="", verifyError="", emailError=""):
        self.render('signup.html', username=username, password=password, verify=verify, email=email, usernameError=usernameError, passwordError= passwordError, verifyError=verifyError, emailError=emailError)
    def get(self):
        self.write_form()
    def post(self):
        usernameError = ""
        passwordError = ""
        verifyError = ""
        emailError = ""
        
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        
        if not validCheck.valid_username(username):
            usernameError = "Not a valid Username"
        if not validCheck.valid_password(password):
            passwordError = "Not a valid Password"
            
        if not(password == verify):
            verifyError = "Does not match password field"
            
        if not validCheck.valid_email(email) and email:
            emailError = "Not a valid Email"
        
        if ((validCheck.valid_email(email) or not email) and validCheck.valid_password(password) 
                                    and validCheck.valid_username(username) and password==verify):
            u = User.by_name(username)
            if u:
                usernameError = "That user already exists"
            else:
                u = User.register(username, password, email)
                u.put()
                self.login(u)
                self.redirect(url.url['welcome'])
        self.write_form(username,'','',email,usernameError,
                        passwordError,verifyError,emailError)

class Welcome(Handler):
    def get(self):
        if self.user:
            self.render('welcome.html')
        else:
            self.redirect(url.url['login'])
            
class Logout(Handler):
    def get(self):
        self.logout()
        self.redirect(url.url['login'])
            
class Login(Handler):
    def write_form(self, username="", password="", usernameError="", passwordError=""):
        self.render('login.html', username=username, password=password, 
                    usernameError=usernameError, passwordError= passwordError)
    def get(self):
        self.write_form()
    def post(self):
        usernameError = ""
        passwordError = ""
        
        username = self.request.get('username')
        password = self.request.get('password')
        
        if not validCheck.valid_username(username):
            usernameError = "Not a valid Username"
        if not validCheck.valid_password(password):
            passwordError = "Not a valid Password"
        
        if validCheck.valid_username(username) and validCheck.valid_password(password):
            u = User.login(username, password)
            if u:
                self.login(u)
                self.redirect(url.url['welcome'])
            else:
                usernameError = "Invalid login"
        self.write_form(username, password, usernameError, passwordError)
app = webapp2.WSGIApplication([(url.url['signup']+r'/?', Signup),
                               (url.url['welcome']+r'/?', Welcome),
                               (url.url['login']+r'/?', Login),
                               (url.url['logout']+r'/?', Logout)],
                              debug=True)
