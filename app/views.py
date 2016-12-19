#from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from flask import Flask, render_template, redirect, url_for, request, Response, flash, jsonify, send_file, send_from_directory, g
from flask_sqlalchemy import SQLAlchemy
#from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from sqlalchemy.orm import sessionmaker
from werkzeug.exceptions import abort
#from passlib.hash import sha256_crypt
from sqlalchemy import create_engine
from models import DBconn, User
from sqlalchemy.orm import exc
from datetime import datetime
from app import app, db
#from forms import *
import hashlib
import sys, os


@app.route('/')
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
			recs.append({'restaurant_id': str(r[0]), 'location_id': r[1], 'restaurant_name': r[2], 'restaurant_info': r[3], 'restaurant_address': r[4], 'restaurant_number': r[5], 'is_active': str(r[6])})
		if len(recs) == 0:
			return jsonify({'status': 'no entries', 'count': len(recs)})
		return jsonify({'status': 'ok', 'entries': recs, 'count': len(recs)})
	else:
		res = spcall('get_restaurant_by_location', passed[:1], True)
		for r in res:
			recs.append({'restaurant_id': str(r[0]), 'location_id': r[1], 'restaurant_name': r[2], 'restaurant_info': r[3], 'restaurant_address': r[4], 'restaurant_number': r[5], 'is_active': str(r[6])})
		if len(recs) == 0:
			return jsonify({'status': 'no entries', 'count': len(recs)})
		return jsonify({'status': 'ok', 'entries': recs, 'count': len(recs)})
####################################################################################

############################## ORDER ######################################



@app.route('/api/order', methods=['GET'])
def get_all_order():
    """ Retrieves all private messages in the database """

    res = spcall('list_orders', ())
    if 'Error' in str(res[0][0]):
        return jsonify({'status': 'error', 'message': res[0][0]})

    recs = []
    for r in res:
    	recs.append({'order id': r[0], 'user id': r[1], 'food id': r[2], 'is_active': r[3]})
	return jsonify({'status': 'ok', 'entries': recs, 'count': len(recs)})


@app.route('/api/order/', methods=['POST'])
def add_transactions():
    """ Add a new private message using a stored procedure """
    
    mess = spcall('list_orders_database', ())
    orderid = len(mess) +1
    
    res = spcall('add_order', (orderid, usesrid, foodid, ), True)
    if 'Error' in str(res[0][0]):
        return jsonify({'status': 'error', 'message': res[0][0]})
         
	return jsonify({'status': 'ok', 'message': ''})



@app.route('/api/transaction/<int:order_id>', methods=['PUT'])
def delete_order(order_id):
	""" Delete a feedback """
	
	# List all feedback id
	order_list = spcall('list_orders', ())
	active_order_ids = []
	for order in order_list:
		active_order_ids.append(order[0])  

	valid_order_id = False

	# Validate feedback id
	for entry in active_order_ids:
		if (entry == order_id):
			valid_order_id = True

	if (valid_order_id):
		res = spcall('delete_order', str(order_id), True)
		return jsonify({'status': 'successful', 'message': 'order successfully removed'})

	return jsonify({'status': 'error', 'message': 'an error was encountered'})



####################################################################################



########################### TRANSACTION #################################


@app.route('/api/transaction', methods=['GET'])
def get_all_transaction():
    """ Retrieves all private messages in the database """

    res = spcall('list_transactions', ())
    if 'Error' in str(res[0][0]):
        return jsonify({'status': 'error', 'message': res[0][0]})

    recs = []
    for r in res:
        recs.append({'transaction id': r[0], 'order id': r[1], 'total bill': r[2], 'datetransact': r[3], 'is_active': r[4]})
	return jsonify({'status': 'ok', 'entries': recs, 'count': len(recs)})


@app.route('/api/transaction/<int:order_id>', methods=['GET'])
def get_transaction(receiverid):
    """ Retrieves all private messages from a receiver who matches the receiver id parameter """

    res = spcall('show_transactions', [str(orderid)])
        

    recs = []
    for r in res:
        recs.append({'transaction id': r[0], 'order id': r[1], 'total bill': r[2], 'datetransact': r[3], 'is_active': r[4]})
    if len(recs) == 0:
        return jsonify({'status': 'error', 'message': "message not found"})
	return jsonify({'status': 'ok', 'entries': recs, 'count': len(recs)})



#@app.route('/api/transaction', methods=['POST'])
#def add_transactions():
#    """ Add a new private message using a stored procedure """
    
#    mess = spcall('list_transactions_database', ())
#    transactionid = len(mess) +1
    
#    res = spcall('add_transactions', (transactionid, orderid, totalbill, deliver, foodquantity, foodname), True)
#    if 'Error' in str(res[0][0]):
#        return jsonify({'status': 'error', 'message': res[0][0]})    
#	return jsonify({'status': 'ok', 'message': ''})



@app.route('/api/transaction/<int:order_id>', methods=['PUT'])
def delete_transaction(feedback_id):
	""" Delete a feedback """
	
	# List all feedback id
	transaction_list = spcall('list_transactions', ())
	active_transaction_ids = []
	for transaction in transaction_list:
		active_transaction_ids.append(transaction[0])  

	valid_transaction_id = False

	# Validate feedback id
	for entry in active_transaction_ids:
		if (entry == transaction_id):
			valid_transaction_id = True

	if (valid_transaction_id):
		res = spcall('delete_transactions', str(transaction_id), True)
		return jsonify({'status': 'successful', 'message': 'transaction successfully removed'})

	return jsonify({'status': 'error', 'message': 'an error was encountered'})
####################################################################################