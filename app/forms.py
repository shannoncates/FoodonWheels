from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, Form, TextField, PasswordField, validators
from wtforms.validators import DataRequired, Length


class RegisterForm(Form):
		fname = TextField('First Name', [validators.Length(min=15, max= 30)])
		lname = TextField('Last Name', [validators.Length(min=15, max=30)])
		minitial = TextField('Middle Initial', [validators.Length(1)])
		email = TextField('Email Address', [validators.Length(min=6, max=35)])
		user_location = TextField('User Location', [validators.Length(min=15, max=30)])
		user_contact = TextField('User Contact', [validators.Length(min=15, max=30)])
		password = PasswordField('New Password', [validators.Required(), validators.EqualTo('confirm', message='Passwords must match')])
		confirm = PasswordField('Repeat Password')
		accept_tos = BooleanField('I accept the TOS', [validators.Required()])


class LoginForm(Form):
	email = TextField('Email', [validators.Length(min=6, max=35)])
	password = PasswordField('Password', [validators.Required()])