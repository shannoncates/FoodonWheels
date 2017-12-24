from flask import Flask, send_file, render_template, send_from_directory, jsonify
from app import app
import sys, os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


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

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    """ The homepage """

    return send_from_directory(os.path.join(APP_ROOT, 'static', 'html'), 'index.html')

    

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


@auth.login_required
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

################# FOOD #####################

@auth.login_required
def get_restaurant():
	""" Retrieves all restaurants in the database with is_active = True """

	restaurant_list = spcall('list_restaurants', ())
		
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


@auth.login_required
def get_food():
	""" Retrieves all foods in the database with is_active = True """

	food_list = spcall('list_foods', ())
		
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


###################### USER #########################

@auth.login_required
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


@auth.login_required
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


@auth.login_required
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


@auth.login_required
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


@auth.login_required
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