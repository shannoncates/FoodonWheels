#from flask_wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, Form, TextField, PasswordField, validators
from wtforms.validators import DataRequired, Length



class RegisterForm(Form):
	email = TextField ('Email Address', [validators.Length(min=8, max=25)])
	password = PasswordField('New Password', [validators.Required(), validators.EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('Repeat Password')
	accept_tos = BooleanField('I accept the TOS', [validators.Required()])


class LoginForm(Form):
	email = TextField('Email', [validators.Length(min=8, max=25)])
	password = PasswordField('Password', [validators.Required()])
