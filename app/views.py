from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from flask import Flask, render_template, redirect, url_for, request, Response, flash, jsonify, send_file, send_from_directory, g
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from sqlalchemy.orm import sessionmaker
from werkzeug.exceptions import abort
from passlib.hash import sha256_crypt
from sqlalchemy import create_engine
from models import DBconn, User
from sqlalchemy.orm import exc
from datetime import datetime
#from flask.ext.socketio import emit, join_room, leave_room
from app import app, db
from forms import *
import hashlib
import sys, os



@app.route('/')
#@app.route('/index')
def index():
    return send_file("templates/index.html")


####################   DATABASE CONNECTION   ###################


def spcall(qry, param, commit=False):
    """ Function which communicates with the database """

    try:
        dbo = DBconn()
        cursor = dbo.getcursor()
        cursor.callproc(qry, param)
        res = cursor.fetchall()
        if commit:
            dbo.dbcommit()
        return res
    except:
        res = [('Error: ' + str(sys.exc_info()[0]) + ' '
               + str(sys.exc_info()[1]), )]
    return res


#################################################################


	
###################### SIGN UP #################################
@app.route('/api/registeruser', methods=['POST'])
def register():
	return send_file("templates/signup.html")

	passw = request.form["password"]
	passw = passw + key
	passw = hashlib.md5(passw.encode())
	email = request.form["email"]

	if email == '':
		return jsonify({'status': 'error2', 'message': 'email cannot be blank'})

	email_validity = False
	valid_email_ending = False

	for endings in valid_endings:
		if endings in email:
			valid_email_ending = True

	if "@" in email and valid_email_ending:
		email_validity = True


	if email_validity == False:
		return jsonify({'status': 'error2', 'message': 'invalid email'})



	recs = spcall('list_users', ())
	if 'Error' in str(recs[0][0]):
		return jsonify({'status': 'error', 'message': recs[0][0]})
	for element in recs:
		if email == str(element[0]):
			return jsonify({'status': 'error2', 'message': 'email already exists'})

	res = spcall('add_user', (
		request.form["email"],
		request.form["firstname"],
		request.form["middlei"],
		request.form["lastname"],
		request.form["contactno"],
		request.form["address"],
		passw
		), True)

	if 'Error' in str(res[0][0]):
		return jsonify({'status': 'error', 'message': res[0][0]})
	return jsonify({'status': 'ok', 'message': res[0][0]})

##################################################################