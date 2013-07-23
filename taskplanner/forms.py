from flask.ext.wtf import Form
from wtforms import (StringField,
                     TextAreaField,
                     PasswordField,
                     SelectField,
                     SelectMultipleField,
                     IntegerField,
                     DateField,
                     validators,
                     SubmitField)
import datetime

class LoginForm(Form):
    username = StringField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])

class RoleForm(Form):
    name = StringField('Role Name', [validators.Required()])
    
class UserForm(Form):
    fname = StringField('First Name', [validators.Required()])
    lname = StringField('Last Name', [validators.Required()])
    username = StringField('Username', [validators.Required()])
    email = StringField('E-Mail', [validators.Required(), validators.Email()])
    password = PasswordField('Password', [validators.Required(), validators.EqualTo('confirm')])
    confirm = PasswordField('Repeat Password')
    roles = SelectMultipleField('Roles')

class EditUserForm(UserForm):
    password = PasswordField('Password', [validators.EqualTo('confirm')])
    username = StringField('Username')
    
class DeleteUserForm(Form):
    delete = SubmitField("Delete")
    cancel = SubmitField("Cancel")

class ClientForm(Form):
    name = StringField('Name', [validators.Required()])
    email = StringField('E-Mail', [validators.Required(), validators.Email()])
    company = StringField('Company', [validators.Required()])

class AddProjectForm(Form):
    title = StringField('Title', [validators.Required()])
    description = TextAreaField('Description', [validators.Required()])
    start_date = DateField('Start Date', [validators.Required()], format = '%m/%d/%Y', default=datetime.date.today())
    client = SelectField('Client', [validators.Required()], coerce=int)
    due_date = DateField('Due Date', [validators.Optional()],format = '%m/%d/%Y')

class EditProjectForm(AddProjectForm):
    percent_complete = IntegerField('Percent Complete')

class AddTaskForm(Form):
    title = StringField('Title', [validators.Required()])
    description = TextAreaField('Description', [validators.Optional()])
    project = SelectField('Project', [validators.Required()], coerce=int)
    owner = SelectField('Task Owner', [validators.Required()], coerce=int)
    start_date = DateField('Start Date', [validators.Required()], format='%m/%d/%Y', default=datetime.date.today())
    percent_complete = IntegerField('Percent Complete', [validators.Optional()])
    due_date = DateField('Due Date', [validators.Optional()])
