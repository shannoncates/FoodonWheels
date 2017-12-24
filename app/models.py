from sqlalchemy import create_engine
#from app import db
import os



#class User(db.Model):
#    """ The user model """
    
#    fname = db.Column(db.String(30))
#    lname = db.Column(db.String(30))
#    minitial = db.Column(db.String(1))
#    email = db.Column(db.String(120), unique=True)
#    user_location = db.Column(db.String(30))
#    user_contact = db.Column(db.String(30))
#    password = db.Column(db.String(30))

#    def is_active(self):
#        return True

#    def __init__(self, fname, lname, minitial, email, user_location, user_contact, password):
#        self.fname = fname
#        self.lname = lname
#        self.minitial = minitial
#        self.email = email
#        self.user_location = user_location
#        self.user_contact = user_contact
#        self.password = password

#    def __repr__(self):
#        return self.fname + " " + self.minitial + " " + self.lname

    
    
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