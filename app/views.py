from flask import Flask, send_file, render_template, send_from_directory, jsonify
from flask_httpauth import HTTPBasicAuth
from app import app
from models import DBconn
from sqlalchemy import create_engine
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
import hashlib
import sys, os


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
key = "1290gath43quz1@"
auth = HTTPBasicAuth()

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


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    """ The homepage """

    return send_from_directory(os.path.join(APP_ROOT, 'static', 'html'), 'index.html')


#def verify_token(token):

#    recs = spcall('list_users', ())

#    for element in recs:
#        if token == hashlib.md5( str(element[4] + element[7] ). encode()).hexdigest(): #email + password 
#            return True
#        return False
    

@app.errorhandler(404)
def page_not_found(e):
	""" 404 Page Not Found Handler """

	return jsonify({'status': '404', 'message': 'Sorry, the page you are looking for was not found'})


@app.errorhandler(500)
def internal_server_error(e):
    """ 500 Internal Server Error """

    return jsonify({'status': '500', 'message': 'Internal Server Error'})

@app.route('/')
@app.route('/index')
def index():
	return send_file("templates/index.html")


@app.route('/api/registeruser', methods=['POST'])
def register():

    user_id = len(spcall("list_users", ())) + 1
    fname = request.form["fname"]
    lname = request.form["lname"]
    minitial = request.form["minitial"]
    email = request.form["email"]
    user_location = request.form["user_location"]
    user_contact = request.form["user_contact"]
	password = request.form["password"]
	password = password + key
	password = hashlib.md5(password.encode())
    password = password.hexdigest()
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
		if email == str(element[4]):
			return jsonify({'status': 'error', 'message': 'email already exists'})

    res = spcall("add_user", (user_id, fname, lname, minitial, email, user_location, user_contact, password), True)
    return jsonify({"status: "200", "message": "success"})
	#res = spcall('add_user', (
	#	request.form["email"],
	#	request.form["firstname"],
	#	request.form["middlei"],
	#	request.form["lastname"],
	#	request.form["contactno"],
	#	request.form["address"],
	#	passw
	#	), True)

	#if 'Error' in str(res[0][0]):
	#	return jsonify({'status': 'error', 'message': res[0][0]})
	#return jsonify({'status': 'ok', 'message': res[0][0]})

@app.route('/api/loginuser', methods=['POST'])
def login():
    """ User login function """

    attempted_email = request.form["email"]
    attempted_password = request.form["password"]
    attempted_password = attempted_password + key
    
    attempted_password = hashlib.md5(attempted_password.encode())
    attempted_password = attempted_password.hexdigest()
    
    res = spcall('list_users', ())
    error = True
    
    for element in res:
        # email element[4]
        # password element[5]
        if attempted_email == element[3]:
            userinfo = {'firstname': element[0], 'lastname': element[1], 'middle_initial': element[2], 
            'email': element[3], 'token':hashlib.md5( str(element[0] + element[4] ).encode()).hexdigest()}
            user = User(element[0], element[1], element[2], element[3], element[4])
            stored_password = element[4] # attempted_password should match this
            error = False
                  
    
    if error == True:
        return jsonify({'status': 'error', 'message': 'email does not exist'})
    if (attempted_password == stored_password):
        return jsonify({'status': 'Successful', 'User_Information': userinfo,'message': 'Logged in successfully!'})
    else:
        return jsonify({'status': 'error', 'message': 'password or email is incorrect'})


@app.route('/api/logout')
def logout():
    """ User logout function """
    return jsonify({'status':'ok','message':'logged out'})
