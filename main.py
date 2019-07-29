
import webapp2
import jinja2
import os
import logging
from google.appengine.ext import ndb
from google.appengine.api import users


jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__))
)


class UnitUser(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()

class Task(ndb.Model):
    task_name = ndb.StringProperty(required=True)
    description = ndb.StringProperty(required=True)
    owner = ndb.KeyProperty(kind=UnitUser, required=True)
    # task_check

# unit model class
class Unit(ndb.Model):
    unit_name = ndb.StringProperty(required=True)
    members = ndb.KeyProperty(kind=UnitUser, repeated=True)
    task_keys = ndb.KeyProperty(kind=Task, repeated=True)


class MainPage(webapp2.RequestHandler):
    def get(self):
        template_vars = {

        }
        user = users.get_current_user()
        if user:
            signout_link_html = '<a href="%s">sign out</a>' % (users.create_logout_url('/'))
            email_address = user.email()
            unit_user = UnitUser.query().filter(UnitUser.email == email_address).get()

            if unit_user:

                self.response.write('''
                Welcome %s %s (%s)! <br> %s <br> ''' % (
                unit_user.first_name,
                unit_user.last_name,
                email_address,
                signout_link_html,
                ))
                template = jinja_env.get_template('templates/home.html')
                self.response.write(template.render(template_vars))
            else:
                self.response.write('''
                    Welcome to our site, %s!  Please sign up! <br>
                    <form method="post" action="/">
                    <input type="text" name="first_name" placeholder="Enter First Name">
                    <input type="text" name="last_name" placeholder="Enter Last Name">
                    <input type="submit">
                    </form><br> %s <br>
                    ''' % (email_address, signout_link_html))
        else:

            login_url = users.create_logout_url('/')
            login_html_element = '<a href="%s">Sign in</a>' % login_url

            self.response.write('Please log in.<br>' + login_html_element)

    def post(self):

        user = users.get_current_user()
        unit_user = UnitUser(
            first_name=self.request.get('first_name'),
            last_name=self.request.get('last_name'),
            email=user.email())
        unit_user.put()
        self.response.write('Thanks for signing up, %s! <br><a href="/">Home</a>' % unit_user.first_name)
        template_vars = {

        }

        # template = jinja_env.get_template('templates/home.html')
        # self.response.write(template.render(template_vars))

class EnterPage(webapp2.RequestHandler):
    def get(self):
        template_vars = {

        }
        template = jinja_env.get_template('templates/enter.html')
        self.response.write(template.render(template_vars))
    def post(self):
        user = users.get_current_user()
        email_address = user.email()
        unit_user = UnitUser.query().filter(UnitUser.email == email_address).get()
        new_unit_key = Unit(unit_name=self.request.get("group"), members=[unit_user.key]).put()
        template_vars = {
            "unit_name": self.request.get("group"),
        }
        template = jinja_env.get_template('templates/enter.html')
        self.response.write(template.render(template_vars))


class IndividualPage(webapp2.RequestHandler):
    def get(self):
        template_vars = {
        
        }
        template = jinja_env.get_template('templates/individual.html')
        self.response.write(template.render(template_vars))



class TaskPage(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/task.html')
        self.response.write(template.render(template_vars))
    def post(self):
        unit_name = self.request.get("group")
        unit_query = Unit.query().filter(Unit.unit_name==unit_name).fetch()
        template_vars = {
            "unit_key": unit_query
        }
        template = jinja_env.get_template('templates/task.html')
        self.response.write(template.render(template_vars))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/enter', EnterPage),
    ('/individual', IndividualPage),
    ('/task', TaskPage),
], debug = True)
