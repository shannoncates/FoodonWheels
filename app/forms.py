from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, Form, TextField, PasswordField, validators
from wtforms.validators import DataRequired, Length

class RegisterForm(Form):
	username = TextField('Username', [validators.Length(min=4, max=25)])
	email = TextField('Email Address', [validators.Length(min=6, max=35)])
	password = PasswordField('New Pssword', [validators.Required()])
	accept_tos = BooleanField('I accept the TOS', [validators.Required()])

class LoginForm():
	username = TextField('Email', [validators.Length(min=4, max=25)])
	password = PasswordField('Password', [validators.Required()])