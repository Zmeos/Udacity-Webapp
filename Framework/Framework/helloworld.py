import webapp2
import framework

class world(framework.Handler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.write('Hello, World Wide Web!')

app = webapp2.WSGIApplication([('/helloworld/?', world)],
                              debug=True)