from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, SelectMultipleField, validators

class LoginForm(Form):
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])

class RoleForm(Form):
    name = TextField('Role Name', [validators.Required()])
    
class UserForm(Form):
    fname = TextField('First Name', [validators.Required()])
    lname = TextField('Last Name', [validators.Required()])
    username = TextField('Username', [validators.Required()])
    email = TextField('E-Mail', [validators.Required(), validators.Email()])
    password = PasswordField('Password', [validators.Required(), validators.EqualTo('confirm')])
    confirm = PasswordField('Repeat Password')
    roles = SelectMultipleField('Roles')

class EditUserForm(UserForm):
    password = PasswordField('Password', [validators.EqualTo('confirm')])
    username = TextField('Username')
