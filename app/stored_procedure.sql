-- ##### TABLES START HERE ##### --

-- Create the User table

create table "User"
(
	user_id int primary key,
	email text,
	first_name text,
	middle_initial text,
	last_name text,
	password text,
	contact_number text,
	address text,
	is_authenticated boolean default True,
	is_active boolean default True,
	is_anonymous boolean default True
);


-- Create the Location table

create table "Location"
(
	location_id int primary key,
	location_name text,
	is_active boolean default True
);


-- Create the Restaurant table

create table "Restaurant"
(
	restaurant_id int primary key,
	location_id int references "Location",
	restaurant_name text,
	restaurant_info text,
	restaurant_address text,
	restaurant_number text,
	is_active boolean default True
);


-- Create the Food table

create table "Food"
(
	food_id int primary key,
	restaurant_id int references "Restaurant",
	food_name text,
	food_info text,
	food_price text,
	food_quantity text,
	is_active boolean default True
);

-- ##### TABLES END HERE ##### --



-- ##### USER STORED PROCEDURES START HERE ##### --

-- (1) Retrieve all users (GET)
create function list_users(out int, out text, out text, out text, out text, out text, out text, out text, out boolean, out boolean, out boolean) returns setof record as
$$
	select user_id, email, first_name, middle_initial, last_name, password, contact_number, address, is_authenticated, is_active, is_anonymous
	from "User";
$$
	language 'sql';

	
-- (2) Add a new user (POST)
create function add_user(par_userid int, par_email text, par_firstname text, par_middlei text, par_lastname text, par_passw text, par_contactno text, par_address text) returns void as
$body$
	begin
		insert into "User" values (par_userid, par_email, par_firstname, par_middlei, par_lastname, par_passw, par_contactno, par_address, True, True, True);
	end
$body$
	language 'plpgsql';


-- (3) Retrieve a user (GET)
create function get_user(in par_user_id int, out int, out text, out text, out text, out text, out text, out text, out text, out boolean, out boolean, out boolean) returns setof record as
$$
	select user_id, email, first_name, middle_initial, last_name, password, contact_number, address, is_authenticated, is_active, is_anonymous
	from "User";
	where user_id = par_user_id;
$$
	language 'sql';


-- (4) Update a user (PUT)
create function update_user(par_userid int, par_email text, par_firstname text, par_middlei text, par_lastname text, par_passw text, par_contactno text, par_address text) returns void as
$$
	update "User"
	set email = par_email, first_name = par_firstname, middle_initial = par_middlei, last_name = par_lastname, password = par_passw, contact_number = par_contactno, address = par_address
	where user_id = par_userid;
$$
	language 'sql';

-- ##### USER STORED PROCEDURES END HERE ##### --


-- ##### LOCATION STORED PROCEDURES START HERE ##### --

-- (1) Retrieve all locations in the database (GET)
create function list_locations(out int, out text) returns setof record as
$$
	select location_id, location_name
	from "Location"
	where is_active = True;
$$
	language 'sql';


-- (2) Get the location which matches the location id parameter (GET)
create function get_location(in par_location_id int, out int, out text) returns setof record as
$$
	select location_id, location_name
	from "Location"
	where is_active = True and location_id = par_location_id;
$$
	language 'sql';


-- (3) Retrieve certain string (GET)
create function get_location_starting_with(in par_keyword text, out int, out text, out boolean) returns setof record as
$$
	select location_id, location_name, is_active
	from "Location"
	where lower(location_name) Like par_keyword;
$$
	language 'sql';

-- ##### LOCATION STORED PROCEDURES END HERE ##### --



-- ##### RESTAURANT STORED PROCEDURES START HERE ##### --

-- (1) Retrieve all restaurants in the database (GET)
create function list_restaurants(out int, out int, out text, out text, out text, out text) returns setof record as
$$
	select restaurant_id, location_id, restaurant_name, restaurant_info, restaurant_address, restaurant_number
	from "Restaurant"
	where is_active = True;
$$
	language 'sql';


-- (2) Retrieve certain restaurant (GET)
create function get_restaurant(in par_restaurant_id int, out int, out int, out text, out text, out text, out text) returns setof record as
$$
	select restaurant_id, location_id, restaurant_name, restaurant_info, restaurant_address, restaurant_number
	from "Restaurant"
	where is_active = True and restaurant_id = par_restaurant_id;
$$
	language 'sql';

-- (3) Retrieve restaurant by location (GET)
create function get_restaurant_by_location(in par_location_id int, out int, out int, out text, out text, out text, out text) returns setof record as
$$
	select restaurant_id, location_id, restaurant_name, restaurant_info, restaurant_address, restaurant_number
	from "Restaurant" 
	where is_active = True and location_id = par_location_id;
$$
	language 'sql';

--(4) Retrieve starting with a certain string(GET)
create function get_restaurant_starting_with(in par_keyword text, out int, out int, out text, out text, out text, out text, out boolean) returns setof record as
$$
	select restaurant_id, location_id, restaurant_name, restaurant_info, restaurant_address, restaurant_number is_active
	from "Restaurant"
	where lower(restaurant_name) Like par_keyword;
$$
	language 'sql';

-- ##### RESTAURANT STORED PROCEDURES END HERE ##### --



-- ##### FOOD STORED PROCEDURES START HERE ##### --

-- (1) Retrieve all foods in the database
create function list_foods(out int, out int, out text, out text, out text, out text) returns setof record as
$$
	select food_id, restaurant_id, food_name, food_info, food_price, food_quantity
	from "Food"
	where is_active = True;
$$
	language 'sql';


-- (2) Retrieve all foods from the restaurant who matches the restaurant id parameter (GET)
create function get_food_by_restaurant(in par_restaurant_id int, out int, out int, out text, out text, out text, out text) returns setof record as
$$
	select food_id, restaurant_id, food_name, food_info, food_price, food_quantity
	from "Food" 
	where is_active = True and restaurant_id = par_restaurant_id;
$$
	language 'sql';


-- (2) Add food to tray (POST)
create function add_food(par_food_id int, par_restaurant_id int, par_food_name text, par_food_info text, par_food_price text, par_food_quantity text) returns void as
$body$
	begin
		insert into "Food" values (par_food_id, par_restaurant_id, par_food_name, par_food_info, par_food_price, par_food_quantity, True);
	end
$body$
	language 'plpgsql';


-- (3) Remove food to tray (DELETE)
create function delete_food(in par_food_id int) returns void as
$$
	update "Food"
	set is_active = False
	where food_id = par_food_id;
$$
	language 'sql';

-- ##### FOOD STORED PROCEDURES END HERE ##### --