from flask import Flask, render_template, send_from_directory, jsonify, request, url_for
from app import app
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from models import DBconn
import hashlib
import sys


######### DATABASE CONNECTION #####################

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

###################################################
    

@app.errorhandler(404)
def page_not_found(e):
	""" 404 Page Not Found Handler """

	return jsonify({'status': '404', 'message': 'Sorry, the page you are looking for was not found'})


@app.errorhandler(500)
def internal_server_error(e):
    """ 500 Internal Server Error """

    return jsonify({'status': '500', 'message': 'Internal Server Error'})

@app.route("/", methods=["GET"])
def index():
	return render_template("index.html")

@app.route("/signin", methods=["GET"])
def signin():
	return render_template("signin.html")

@app.route("/signup", methods=["GET"])
def signup():
	return render_template("signup.html")

@app.route("/userprofile", methods=["GET"])
def userprofile():
	return render_template("userprofile.html")

@app.route("/about", methods =["GET"])
def about():
	return render_template("about.html")

@app.route("/signout", methods=["GET"])
def signout():
	return render_template("index.html")

@app.route("/sidebarright", methods=["GET"])
def sidebarright():
	return render_template("sidebar-right.html")

@app.route("/sidebarleft", methods=["GET"])
def sidebarleft():
	return render_template("sidebar-left.html")

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

	if email == '':
		return jsonify({'status': 'error', 'message': 'email cannot be blank'})

	email_validity = False
	valid_email_ending = False

	for endings in valid_endings:
		if endings in email:
			valid_email_ending = True

	if "@" in email and valid_email_ending:
		email_validity = True


	if email_validity == False:
		return jsonify({'status': 'error', 'message': 'invalid email'})

	recs = spcall('list_users', ())

	if 'Error' in str(recs[0][0]):
		return jsonify({'status': 'error', 'message': recs[0][0]})
	for element in recs:
		if email == str(element[0]):
			return jsonify({'status': 'error', 'message': 'email already exists'})

	res = spcall("add_user", (user_id, fname, lname, minitial, email, user_location, user_contact, password), True)
	return jsonify({"status": "200", "message": "success"})

@app.route('/api/loginuser', methods=['POST'])
def login():
    """ User login function """

    email = request.form["email"]
    password = request.form["password"]
    password = password + key
    password = hashlib.md5(password.encode())
    password = password.hexdigest()

    if ((email == "") or (password == "")):
		return jsonify({"status": "error", "message": "email or password is incorrect"})

    res = spcall('list_users', ())
    userinfo = {}
    
    for element in res:
	if ((email == element[4]) and (password == element[7])):
		userinfo = {"id": element[0], "fname": element[1], "lname": element[2], "minitial": element[3], "email": element[4], "user_location": element[5], "user_contact": element[6], "password": element[7]}
	
	if (len(userinfo) == 0):
		return jsonify({"status": "error", "message": "email or password is incorrect"})
	else:
		return jsonify({"status": "200", "userinfo": userinfo, "message": "signed in"})


#@auth.login_required
@app.route('/api/logout')
def logout():
    """ User logout function """
    return jsonify({'status':'ok','message':'logged out'})


########### LISTS #####################
    
    # List all user_id numbers
    users = spcall('list_users', ())
    user_id_list = []
    for user in users:
        user_id_list.append(user[0])
        
    # List all restaurant_id numbers
    restaurants = spcall('list_restaurants', ())
    restaurant_id_list = []
    for restaurant in restaurants:
        restaurant_id_list.append(restaurant[0])

    # List all food_id numbers
    foods = spcall('list_foods', ())
    food_id_list = []
    for food in foods:
        food_id_list.append(food[0])

# ====================================================================================
@app.route("/api/user", methods = ["put"])
def update_user():
    """ the update user function """

    id = request.form["id"]
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
    
    if email == '':
        return jsonify({'status': 'error', 'message': 'email cannot be blank'})
    
    email_validity = False
    valid_email_ending = False
    
    
    for endings in valid_endings:
        if endings in email:
            valid_email_ending = True
            
    if ("@" in email) and valid_email_ending:
        email_validity = True    
        
    if  email_validity == False:
        return jsonify({'status': 'error', 'message': 'invalid email'})    
    
    recs = spcall('list_users', ())
    
    if 'Error' in str(recs[0][0]):
        return jsonify({'status': 'error', 'message': "error in list_users sp"})
    for element in recs:
        if email == str(element[4]):     # email
            return jsonify({'status': 'error', 'message': 'email already exists'})

    res = spcall("update_user", (id, fname, lname, minitial, email, user_location, user_contact, password ), True)

    if "Error" in str(res[0][0]):
        return jsonify({"status": "error", "message": res[0][0]})
    else:
        return jsonify({"status": "200", "message": "success"})


################# FOOD #####################

#@auth.login_required
def get_restaurant():
	""" Retrieves all restaurants in the database with is_active = True """

	restaurant_list = spcall('list_restaurant', ())
		
	if (len(restaurant_list) == 0):
		return jsonify({'status': 'successful', 'message': 'empty'})
		
	else:
		recs = []
		for i in restaurant_list:
			recs.append({'restaurant_id': i[0], 
                         'user_id_number': i[1], 
                         'restaurant_name': i[2], 
                         'restaurant_contact': i[3],
                         'restaurant_email': i[4],
                         'restaurant_address': i[5],
                         'restaurant_description': i[6]})
            
		return jsonify({'status': 'successful', 'entries': recs, 'count': len(recs)})

#@auth.login_required
@app.route('/api/restaurant/<int:restaurant_id>', methods=['PUT'])
def delete_restaurant(restaurant_id):
	""" Delete a restaurant """
	
	# List all restaurant id
	restaurant_list = spcall('list_restaurant', ())
	active_restaurant_ids = []
	for restaurant in restaurant_list:
		active_restaurant_ids.append(restaurant[0])  

	valid_restaurant_id = False

	# Validate restaurant id
	for entry in active_restaurant_ids:
		if (entry == restaurant_id):
			valid_restaurant_id = True

	if (valid_restaurant_id):
		res = spcall('delete_restaurant', str(restaurant_id), True)
		return jsonify({'status': 'successful', 'message': 'restaurant successfully removed'})

	return jsonify({'status': 'error', 'message': 'an error was encountered'})


############################################################################################


#@auth.login_required
def get_food():
	""" Retrieves all foods in the database with is_active = True """

	food_list = spcall('list_food', ())
		
	if (len(food_list) == 0):
		return jsonify({'status': 'successful', 'message': 'empty'})
		
	else:
		recs = []
		for i in food_list:
			recs.append({'food_id': i[0], 
                         'user_id_number': i[1],
                         'restaurant_id_number': i[2], 
                         'food_name': i[3], 
                         'food_cost': i[4],
                         'food_description': i[5]})
            
		return jsonify({'status': 'successful', 'entries': recs, 'count': len(recs)})

#s@auth.login_required
@app.route('/api/food/<int:food_id>', methods=['PUT'])
def delete_food(food_id):
	""" Delete a food """
	
	# List all food id
	food_list = spcall('list_food', ())
	active_food_ids = []
	for food in food_list:
		active_food_ids.append(food[0])  

	valid_food_id = False

	# Validate food id
	for entry in active_food_ids:
		if (entry == food_id):
			valid_food_id = True

	if (valid_food_id):
		res = spcall('delete_food', str(food_id), True)
		return jsonify({'status': 'successful', 'message': 'food successfully removed'})

	return jsonify({'status': 'error', 'message': 'an error was encountered'})


############################################################################################


###################### USER #########################

#@auth.login_required
@app.route('/api/user', methods=['GET'])
def get_users():
    """ Retrieves all users stored in the database """

    res = spcall('list_users', ())
    if 'Error' in str(res[0][0]):
        return jsonify({'status': 'error', 'message': res[0][0]})

    recs = []
    for r in res:
        recs.append({'user_id': r[0], 'fname': r[1], 'lname': r[2], 'minitial': r[3], 'email': r[4], 'user_location': r[4], 'user_contact': r[5], 'password': r[6], 'is_active': r[7], 'is_anonymous': r[8], 'role': r[9]})
    return jsonify({'status': 'ok', 'entries': recs, 'count': len(recs)})

#####################################################




######################################   FEEDBACK   ########################################


#@auth.login_required
def add_feedback():
    """ Add a new feedback """

    if ((request.form["body"] == '') or (request.form["user_id"] == '') or (request.form["restaurant_id"] == '')):
        return jsonify({'status': 'error', 'message': 'Incomplete submission'})

    else:
		body = request.form["body"]
		user_id = request.form["user_id"]
		restaurant_id = int(request.form["restaurant_id"])

		# List all restaurant id
		restaurants = spcall('list_restaurants', ())
		restaurant_id_list = []
		for restaurant in restaurants:
			restaurant_id_list.append(restaurant[0])
    
		# List all id numbers
		users = spcall('list_users', ())
		user_id_list = []
		for user in users:
			user_id_list.append(user[0])

		valid_user_id = False
		valid_restaurant_id = False

		# Validate restaurant id
		for entry in restaurant_id_list:
			if (entry == restaurant_id):
				valid_restaurant_id = True

		# Validate user id
		for entry in user_id_list:
			if (entry == user_id):
				valid_user_id = True

		if (valid_user_id and valid_restaurant_id):
			feedback_id = len(spcall('list_feedback_database', ())) + 1
			res = spcall('add_feedback', (feedback_id, restaurant_id, user_id, body), True)
		
			return jsonify({'status': 'successful', 'message': 'feedback successfully added'})

		else:
			return jsonify({'status': 'error', 'message': 'an error was encountered'})


#@auth.login_required
def get_feedback_by_restaurant(restaurant_id):
	""" Retrieve all feedback of a particular restaurant """

	# List all restaurant id
	restaurant_list = spcall('list_restaurants', ())
	active_restaurant_ids = []
	for restaurant in restaurant_list:
		active_restaurant_ids.append(restaurant[0])
        
	valid_restaurant_id = False
    
	# Validate restaurant id
	for entry in active_restaurant_ids:
		if (entry == restaurant_id):
			valid_restaurant_id = True
	
	if (valid_restaurant_id):
		res = spcall('list_feedback_by_restaurant', str(restaurant_id))
		if (len(res) == 0):
			return jsonify({'status': 'successful', 'message': 'empty'})
		else:
			recs = []
			for i in res:
				recs.append({'feedback_id': str(i[0]), 'restaurant_id': str(i[1]), 'user_id': i[2], 'body': i[3], 'date_published': i[4]})
			return jsonify({'status': 'successful', 'entries': recs, 'count': len(recs)})
			
	else:
		return jsonify({'status': 'error', 'message': 'an error was encountered'})


#@auth.login_required
def edit_feedback(restaurant_id, feedback_id):
	""" Edit a particular feedback """

	if ((request.form["body"] == '') or (request.form["user_id"] == '')):
		return jsonify({'status': 'error', 'message': 'Incomplete submission'})

	else:
		# List all restaurant id
		restaurant_list = spcall('list_restaurants', ())
		active_restaurant_ids = []
		for restaurant in restaurant_list:
			active_restaurant_ids.append(restaurant[0])

		# List all feedback id
		feedback_list = spcall('list_feedback', ())
		active_feedback_ids = []
		for feedback in feedback_list:
			active_feedback_ids.append(feedback[0]) 

		valid_restaurant_id = False
		valid_feedback_id = False

		# Validate restaurant id
		for entry in active_restaurant_ids:
			if (entry == restaurant_id):
				valid_restaurant_id = True

		# Validate feedback id
		for entry in active_feedback_ids:
			if (entry == feedback_id):
				valid_feedback_id = True
    
		if (valid_restaurant_id and valid_feedback_id):
			res = spcall('edit_feedback', (feedback_id, request.form["body"]), True)
			return jsonify({'status': 'successful', 'message': 'feedback successfully updated'})
	
		else:
			return jsonify({'status': 'error', 'message': 'an error was encountered'})


#@auth.login_required
def delete_feedback(feedback_id):
	""" Delete a feedback """
	
	# List all feedback id
	feedback_list = spcall('list_feedback', ())
	active_feedback_ids = []
	for feedback in feedback_list:
		active_feedback_ids.append(feedback[0])  

	valid_feedback_id = False

	# Validate feedback id
	for entry in active_feedback_ids:
		if (entry == feedback_id):
			valid_feedback_id = True

	if (valid_feedback_id):
		res = spcall('delete_feedback', str(feedback_id), True)
		return jsonify({'status': 'successful', 'message': 'feedback successfully removed'})

	return jsonify({'status': 'error', 'message': 'an error was encountered'})


############################################################################################

#@auth.login_required
@app.route('/profilepictures/<string:idnumber>', methods=['GET'])
def get_profile_picture(idnumber):
    """ Retrieve the filename of the current profile picture """

    res = spcall('get_profilepicture', [str(idnumber)])
    
    for i in res:
        filename = i[0]

    return jsonify({'filename': filename})


#@auth.login_required
@app.route('/profilepicture/<string:idnumber>', methods=['POST'])
def upload_profile_picture(idnumber):
    """ Upload profile picture """

    ################ GET THE LATEST VERSION OF THE IMAGE ##############
    res = spcall('get_profilepicture', [str(idnumber)])
    rec = []
    for i in res:
        rec.append({'filename': i[0]})

    print ("location")
    pro = rec[0]
    print (pro)
    pro = str(pro)
    print ("pro")
    print (pro)
    pro = pro[-3:]
    pro = pro[0]
    print (pro)
    version = pro
    version = int(version)
    version = version + 1
    version = str(version)

    #################   UPLOAD THE NEW PHOTO   #################
    
    target = os.path.join(APP_ROOT, 'static/profile_pictures/')

    # If the upload directory does not exist, create it:
    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist('photo'):
        print (file)
        filename = idnumber + version
        print (filename)
        destination = '/'.join([target, filename])
        print (destination)
        file.save(destination)

    # Save the filename of the profile picture into the database
    res = spcall('uploadprofilepicture', (idnumber, destination), True)
    res = spcall('updateprofilepicture', (idnumber, destination), True)
    print (destination)

    return jsonify({'status': 'success', 'message': 'Profile Picture Uploaded Successfully'})


#####################################################################################

#@auth.login_required
@app.route('/restaurantpictures/<string:idnumber>', methods=['GET'])
def get_restaurant_picture(idnumber):
    """ Retrieve the filename of the current restaurant picture """

    res = spcall('get_restaurantpicture', [str(idnumber)])
    
    for i in res:
        filename = i[0]

    return jsonify({'filename': filename})


#@auth.login_required
@app.route('/restaurantpicture/<string:idnumber>', methods=['POST'])
def upload_restaurant_picture(idnumber):
    """ Upload restaurant picture """

    ################ GET THE LATEST VERSION OF THE IMAGE ##############
    res = spcall('get_restaurantpicture', [str(idnumber)])
    rec = []
    for i in res:
        rec.append({'filename': i[0]})

    print ("location")
    pro = rec[0]
    print (pro)
    pro = str(pro)
    print ("pro")
    print (pro)
    pro = pro[-3:]
    pro = pro[0]
    print (pro)
    version = pro
    version = int(version)
    version = version + 1
    version = str(version)

    #################   UPLOAD THE NEW PHOTO   #################
    
    target = os.path.join(APP_ROOT, 'static/restaurant_pictures/')

    # If the upload directory does not exist, create it:
    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist('photo'):
        print (file)
        filename = idnumber + version
        print (filename)
        destination = '/'.join([target, filename])
        print (destination)
        file.save(destination)

    # Save the filename of the restaurant picture into the database
    res = spcall('uploadrestaurantpicture', (idnumber, destination), True)
    res = spcall('updaterestaurantpicture', (idnumber, destination), True)
    print (destination)

    return jsonify({'status': 'success', 'message': 'Restaurant Picture Uploaded Successfully'})


#####################################################################################

#@auth.login_required
@app.route('/foodpictures/<string:idnumber>', methods=['GET'])
def get_food_picture(idnumber):
    """ Retrieve the filename of the current food picture """

    res = spcall('get_foodpicture', [str(idnumber)])
    
    for i in res:
        filename = i[0]

    return jsonify({'filename': filename})


#@auth.login_required
@app.route('/foodpicture/<string:idnumber>', methods=['POST'])
def upload_food_picture(idnumber):
    """ Upload food picture """

    ################ GET THE LATEST VERSION OF THE IMAGE ##############
    res = spcall('get_foodpicture', [str(idnumber)])
    rec = []
    for i in res:
        rec.append({'filename': i[0]})

    print ("location")
    pro = rec[0]
    print (pro)
    pro = str(pro)
    print ("pro")
    print (pro)
    pro = pro[-3:]
    pro = pro[0]
    print (pro)
    version = pro
    version = int(version)
    version = version + 1
    version = str(version)

    #################   UPLOAD THE NEW PHOTO   #################
    
    target = os.path.join(APP_ROOT, 'static/food_pictures/')

    # If the upload directory does not exist, create it:
    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist('photo'):
        print (file)
        filename = idnumber + version
        print (filename)
        destination = '/'.join([target, filename])
        print (destination)
        file.save(destination)

    # Save the filename of the food picture into the database
    res = spcall('uploadfoodpicture', (idnumber, destination), True)
    res = spcall('updatefoodpicture', (idnumber, destination), True)
    print (destination)

    return jsonify({'status': 'success', 'message': 'Food Picture Uploaded Successfully'})


#####################################################################################