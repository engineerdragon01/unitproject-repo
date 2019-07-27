
import webapp2
import jinja2
import os

env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__))
)



app = webapp2.WSGIApplication([
], debug = True)
