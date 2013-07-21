from flask.ext.wtf import Form
from wtforms import (StringField,
                     TextAreaField,
                     PasswordField,
                     SelectField,
                     SelectMultipleField,
                     DateField,
                     validators,
                     SubmitField)

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
    startdate = DateField('Start Date', [validators.Required()], format = '%m/%d/%Y')
    client = SelectField('Client', [validators.Required()], coerce=int)
    due_date = DateField('Due Date', [validators.Optional()],format = '%m/%d/%Y')
    
class AddTaskForm(Form):
    pass
