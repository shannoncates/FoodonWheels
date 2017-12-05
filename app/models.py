from sqlalchemy import create_engine
from app import db
import os



class User(db.Model):
    """ The user model """
    
    first_name = db.Column(db.String(30), primary_key=True)
    last_name = db.Column(db.String(30))
    middle_initial = db.Column(db.String(1))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(30))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def __init__(self, first_name, last_name, middle_initial, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.middle_initial = middle_initial
        self.email = email
        self.password = password

    def __repr__(self):
        return self.first_name + " " + self.middle_initial + " " + self.last_name

    
    
class DBconn:
    """ Database Connection """
    
    def __init__(self):
		engine = create_engine("postgresql+psycopg2://postgres:cheche002@localhost/foodonwheels", echo=False)
		self.conn = engine.connect()
		self.trans = self.conn.begin()

    def getcursor(self):
		cursor = self.conn.connection.cursor()
		return cursor

    def dbcommit(self):
		self.trans.commit()