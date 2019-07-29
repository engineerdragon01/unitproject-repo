
import webapp2
import jinja2
import os
import logging
from google.appengine.ext import ndb
from google.appengine.api import users


jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__))
)
class MainPage(webapp2.RequestHandler):
    def get(self):
        template_vars = {

        }
        template = jinja_env.get_template('templates/home.html')
        self.response.write(template.render(template_vars))

class IndividualPage(webapp2.RequestHandler):
    def get(self):
        template_vars = {

        }
        template = jinja_env.get_template('templates/login.html')
        self.response.write(template.render(template_vars))

class TaskPage(webapp2.RequestHandler):
    def get(self):
        template_vars = {

        }
        template = jinja_env.get_template('templates/task.html')
        self.response.write(template.render(template_vars))

class QueuePage(webapp2.RequestHandler):
    def get(self):
        template_vars = {

        }
        template = jinja_env.get_template('templates/queue.html')
        self.response.write(template.render(template_vars))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/individual', IndividualPage),
    ('/task', TaskPage),
    ('/queue', QueuePage),
], debug = True)
