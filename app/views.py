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
from app import app, db
from forms import *
import hashlib
import sys, os


############   GLOBAL ITEMS   ############


auth = HTTPTokenAuth("bearer")
login_manager = LoginManager()
login_manager.init_app(app)
key = "1290gath43quz1@"
#ALLOWED_EXTENSIONS = set(['pdf', 'docx', 'odt'])
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
valid_endings = [".com",".edu",".ph",".net",".gov"] # valid endings for email


##########################################


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



@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    return send_from_directory(os.path.join(APP_ROOT, 'static', 'html'), 'index.html')


@auth.verify_token
def verify_token(token):

	recs = spcall('list_users', ())

	for element in recs:
		if token == hashlib.md5( str(element[1] + element[5] ).encode()).hexdigest(): #email + password
			return True
		return False


@app.errorhandler(404)
def page_not_found(e):
	""" 404 Page Not Found Handler """

	return jsonify({'status': '404', 'message': 'Sorry, the page you are looking for was not found'})


@app.errorhandler(500)
def internal_server_error(e):
	""" 500 Internal Server Error """

	return jsonify({'status': '500', 'message': 'Internal Server Error'})
###################### SIGN UP #################################
@app.route('/api/registeruser', methods=['POST'])
def register():

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


###################### LOG IN - LOG OUT #################################
@app.route('/api/login', methods=['POST'])
def authentication():
    data = json.loads(request.data)
    password = data['password']

    pw_hash = hashlib.md5(password.encode())

    login = spcalls.spcall("list_users", (data['email'], pw_hash.hexdigest()))

    if data['email'] == '' or not password:
        return jsonify({'status': 'FAILED', 'message': 'Invalid email or password'})

    if login[0][0] == 'ERROR':
        status = False
        return jsonify({'status': status, 'message': 'error'})
    else:
        status = True
	return jsonify({'status': status, 'message': 'Successfully Logged In'})

@app.route('/api/logout')
def logout():
    """ User logout function """
    return jsonify({'status':'ok','message':'logged out'})


#######################################################


########## RESTAURANT ##########
@app.route('/api/restaurant/location/<int:location_id>', methods=['GET'])
def get_restaurant_location(location_id):

	location_list = spcall('list_locations', ())
	matched_restaurant = spcall('get_restaurant_by_location', [str(location_id)])

	if ((location_id > len(location_list)) or (location_id < 1) or (len(matched_restaurant)==0)):
		return jsonify({'status': 'error', 'message': 'no match found'})

	else:
		recs = []
		for i in matched_restaurant:

			recs.append({'restaurant_id': str(i[0]),
					'location_id': str(i[1]),
					'restaurant_name': i[2],
					'restaurant_info': i[3]})

		return jsonify({'status': 'successful', 'match': recs})

#######################################################


########## FOOD ##########
@app.route('/api/food/restaurant/<int:restaurant_id>', methods=['GET'])
def get_food_restaurant(restaurant_id):


	restaurant_list = spcall('list_restaurants', ())
	matched_food = spcall('get_food_by_restaurant', [str(restaurant_id)])

	if ((restaurant_id > len(restaurant_list)) or (restaurant_id < 1) or (len(matched_food)==0)):
		return jsonify({'status': 'error', 'message': 'no match found'})

	else:
		recs = []
		for i in matched_food:

			recs.append({'food_id': str(i[0]),
					'restaurant_id': str(i[1]),
					'food_name': i[2],
					'food_info': i[3],
					'food_price': i[4]})

		return jsonify({'status': 'successful', 'match': recs})

######################################################################


########## SEARCH ##########
@app.route('/api/search', methods=['POST'])
def search():

	"""" Search a restaurant using keyword """
	passedkeyword = request.form["keyword"].lower() + "%"
	passed = [passedkeyword, 0]
	recs = []
	if request.form["keyword"] == "":
			return jsonify({'status': 'no entries', 'count': 0})
	if request.form["searchtype"] == "restaurant":
		res = spcall('get_restaurant_starting_with', passed[:1], True)
		for r in res:
			recs.append({'restaurant_id': str(r[0]), 'location_id': str(r[1]), 'restaurant_name': r[2], 'restaurant_info': r[3], 'restaurant_address': r[4], 'restaurant_number': r[5], 'is_active': str(r[6])})
		if len(recs) == 0:
			return jsonify({'status': 'no entries', 'count': len(recs)})
		return jsonify({'status': 'ok', 'entries': recs, 'count': len(recs)})
	else:
		res = spcall('get_restaurant_by_location', passed[:1], True)
		for r in res:
			recs.append({'restaurant_id': str(r[0]), 'location_id': str(r[1]), 'restaurant_name': r[2], 'restaurant_info': r[3], 'restaurant_address': r[4], 'restaurant_number': r[5], 'is_active': str(r[6])})
		if len(recs) == 0:
			return jsonify({'status': 'no entries', 'count': len(recs)})
		return jsonify({'status': 'ok', 'entries': recs, 'count': len(recs)})
####################################################################################