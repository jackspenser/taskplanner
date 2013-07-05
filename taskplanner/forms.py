from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, validators

class LoginForm(Form):
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])
    