
import webapp2
import jinja2
import os
import logging
import random
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import mail

jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__))
)


class UnitUser(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()

class Task(ndb.Model):
    task_name = ndb.StringProperty(required=True)
    description = ndb.StringProperty(required=False)
    owner = ndb.KeyProperty(kind=UnitUser, required=False)
    finished = ndb.BooleanProperty(default=False)
    # task_check

# unit model class
class Unit(ndb.Model):
    unit_name = ndb.StringProperty(required=True)
    members = ndb.KeyProperty(kind=UnitUser, repeated=True)
    task_keys = ndb.KeyProperty(kind=Task, repeated=True)

    def AssignTasksRandomly(self):
        tasks_keys = self.task_keys
        member_keys = self.members


        for task_key in tasks_keys:
            task = task_key.get()
            task.owner = random.choice(member_keys)
            task.put()
        self.put()





class MainPage(webapp2.RequestHandler):
    def get(self):
        unit_list = Unit.query().fetch()
        user = users.get_current_user()
        email_address = user.email()
        template_vars = {
            "unit_list": unit_list,
            "member_email": email_address,
        }
        #  User is always guaranteed to be logged in because of app.yaml therefore if/else not required
        user = users.get_current_user()
        signout_link_html = '<a href="%s">sign out</a>' % (users.create_logout_url('/'))
        email_address = user.email()
        unit_user = UnitUser.query().filter(UnitUser.email == email_address).get()
        signout_link = (users.create_logout_url('/'))
        template_vars["signout_link"]=signout_link

        if unit_user:
            template_vars["first_name"]=unit_user.first_name
            template_vars["last_name"]=unit_user.last_name
            template = jinja_env.get_template('templates/home.html')
            self.response.write(template.render(template_vars))

        else:
            template = jinja_env.get_template('templates/sign_up.html')
            self.response.write(template.render(template_vars))


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
        new_unit = Unit(unit_name=self.request.get("group"), members=[unit_user.key]).put()
        template_vars = {
            "unit_name": self.request.get("group"),
        }
        template = jinja_env.get_template('templates/enter.html')
        self.response.write(template.render(template_vars))


class IndividualPage(webapp2.RequestHandler):
    def get(self):
        unit_link = ndb.Key(urlsafe=self.request.get("group"))
        unit = unit_link.get()
        user = users.get_current_user()
        email_address = user.email()
        unit_user = UnitUser.query().filter(UnitUser.email == email_address).get()
        template_vars = {
            "unit_link": unit_link,
            "unit": unit,
            "user_email": unit_user.email,
        }
        template = jinja_env.get_template('templates/individual.html')
        self.response.write(template.render(template_vars))

    def post(self):
        unit_key = ndb.Key(urlsafe=self.request.get("unit_key"))
        unit = unit_key.get()
        tasks_keys = unit.task_keys
        for task_key in tasks_keys:
            checkboxvalue = self.request.get(task_key.urlsafe())
            if checkboxvalue == 'on':
                task = task_key.get()
                task.finished = True
                task.put()
        unit.put()
        unit_link = ndb.Key(urlsafe=self.request.get("group"))
        unit = unit_link.get()
        user = users.get_current_user()
        email_address = user.email()
        unit_user = UnitUser.query().filter(UnitUser.email == email_address).get()
        template_vars = {
            "unit_link": unit_link,
            "unit": unit,
            "user_email": unit_user.email,
        }
        template = jinja_env.get_template('templates/individual.html')
        self.response.write(template.render(template_vars))


                #TODO: if checkboxvalue then change the task owner for task_key so it displays in finished tasks according to the jinja in individual page

                # Task = ndb.Key(urlsafe=self.request.get("taskkey.urlsafe()"))





class TaskPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        email_address = user.email()
        unit_user = UnitUser.query().filter(UnitUser.email == email_address).get()

        needle_name = self.request.get("group")
        unit = Unit.query().filter(Unit.unit_name == needle_name).get()
        if unit:
            print('already made')
        else:
            unit = Unit(unit_name=needle_name, members=[unit_user.key])
            unit_key = unit.put()
        template_vars = {
            "unit": unit,
            "unit_name": self.request.get("group"),
            "unit_key": unit.key.urlsafe(),
            "user_in_data": self.request.get("user") == 'True',
        }
        template = jinja_env.get_template('templates/task.html')
        self.response.write(template.render(template_vars))
    def post(self):
        print('hello')
        print(self.request.get("currentname"))
        user_in_data = True
        unit_key = ndb.Key(urlsafe=self.request.get("currentname"))
        needle_task = self.request.get("task")
        added_user_email = self.request.get("user")
        unit = unit_key.get()
        user_objects = UnitUser.query().fetch()
        email_list = []
        members_added = []
        for user in user_objects:
            email_list.append(user.email)
        if needle_task:
            user = users.get_current_user()
            email_address = user.email()
            unit_user = UnitUser.query().filter(UnitUser.email == email_address).get()
            task = Task(task_name=needle_task, owner=unit_user.key)
            task_key = task.put()
            unit.task_keys.append(task_key)
            unit.put()
        if added_user_email in email_list:
            members_added.append(added_user_email)

            if added_user_email and added_user_email not in members_added:
                added_user = UnitUser.query().filter(UnitUser.email == added_user_email).get()
                added_user_key = added_user.put()
                unit.members.append(added_user_key)
                unit.put()
            user_in_data = True
        else:
            user_in_data = False

        self.redirect('/task?group={}&user={}'.format(unit.unit_name, user_in_data))


class AboutPage(webapp2.RequestHandler):
    def get(self):
        template_vars = {

        }
        template = jinja_env.get_template('templates/about.html')
        self.response.write(template.render(template_vars))

class RandomizePage(webapp2.RequestHandler):
    def post(self):
        unit_key = ndb.Key(urlsafe=self.request.get("currentname"))
        unit = unit_key.get()
        unit.AssignTasksRandomly()

        self.redirect('/task?group={}'.format(unit.unit_name))




app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/enter', EnterPage),
    ('/individual', IndividualPage),
    ('/task', TaskPage),
    ('/about', AboutPage),
    ('/randomize_assignment', RandomizePage),
], debug = True)
