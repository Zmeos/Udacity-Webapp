import webapp2

class world(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, World Wide Web!')

app = webapp2.WSGIApplication([('/helloworld/?', world)],
                              debug=True)