from sqlalchemy import create_engine
from app import db
import os



class User(db.Model):
	""" The user model """

	email = db.Column(db.String(30), primary_key=True)
	first_name = db.Column(db.String(30))
	middle_initial = db.Column(db.String(1))
	last_name = db.Column(db.String(30))
	password = db.Column(db.String(30))
	contact_number = db.Column(db.String(30))
	address = db.Column(db.String(30))

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return str (self.email)

	def __init__(self, email, first_name, middle_initial, last_name, password, contact_number, address):
		self.email = email
		self.first_name = first_name
		self.middle_initial = middle_initial
		self.last_name = last_name
		self.password = password
		self.contact_number = contact_number
		self.address = address

	def __repr__(self):
		return self.first_name + " " + self.middle_initial + " " + self.last_name



class DBconn:
	""" Database Connection """

	def __init__(self):
		engine = create_engine("postgresql+psycopg2://postgres:monkeyka19@localhost/DeliverFood", echo=False)
		self.conn = engine.connect()
		self.trans = self.conn.begin()

	def getcursor(self):
		cursor = self.conn.connection.cursor()
		return cursor

	def dbcommit(self):
		self.trans.commit()