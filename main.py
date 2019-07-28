
import webapp2
import jinja2
import os
import logging

jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__))
)
class LoginPage(webapp2.RequestHandler):
    def get(self):
        template_vars = {

        }
        template = jinja_env.get_template('templates/login.html')
        self.response.write(template.render(template_vars))


app = webapp2.WSGIApplication([
    ('/', LoginPage)
], debug = True)
