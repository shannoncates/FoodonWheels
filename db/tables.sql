
create table "User"
(
  user_id int primary key,
  fname text,
  lname text,
  minitial text,
  email text unique,
  user_location text,
  user_contact text,
  password text,
  is_active boolean default True
);

create table "Restaurant"
(
   restaurant_id int primary key,
   restaurant_name text,
   restaurant_contact text,
   restaurant_email text,
   restaurant_address text,
   restaurant_description text,
   is_active boolean default True
);

create table "Food"
(
   food_id int primary key,
   restaurant_id text references "Restaurant",
   food_name text,
   food_cost real,
   food_description text,
   is_active boolean default True
)

create table "Feedbackr"
(
  feedbackr_id int primary key,
  restaurant_id text references "Restaurant",
  user_id text references "User",
  body text,
  date_published timestamp,
  is_active boolean default True
);

create table "Feedbackf"
(
  feedbackf_id int primary key,
  food_id text references "Food",
  user_id text references "User",
  body text,
  date_published timestamp,
  is_active boolean default True
);

create table "Profilepicture"
(
  prof_id text primary key,
  filename text
);

create table "Restaurantpicture"
(
  respic_id text primary key,
  filename text
);

create table "Foodpicture"
(
  foodpic_id text primary key,
  filename text
);

create table "Menuorder"
(
  menuorder_id int primary key,
  food_id text references "Food",
  restaurant_id text references "Restaurant",
  quantity int,
  is_active boolean default True
);

create table "Orders"
(
  order_id int primary key,
  user_id int references "User",
  menuorder_id int references "Menuorder",
  is_active boolean default True
);

create table "Foodtransaction"
(
  foodtrans_id int primary key,
  order_id int references "Orders"
  foodtrans_date timestamp,
  total real,
  is_paid boolean default False
);
-------------------------------------------------------------------------------------------------------------------

create function get_profilepicture(in par_id_number text, out text) returns text as
$$
  select filename
  from "Profilepicture"
  where prof_id = par_id_number;
$$
  language 'sql';


create function updateprofilepicture(in par_id_number text, in par_filename text) returns void as
$$
  update "Profilepicture"
    set filename = par_filename
    where prof_id = par_id_number;
$$
  language 'sql';


create function uploadprofilepicture(user_id text, filename text) returns void as
$$
  begin
    insert into "Profilepicture" values (prof_id, filename);
  end
$$
  language 'plpgsql';
--------------------------------------------------------------------------------------------------------------------

create function get_restaurantpicture(in par_id_number text, out text) returns text as
$$
  select filename
  from "Restaurantpicture"
  where respic_id = par_id_number;
$$
  language 'sql';


create function updaterestaurantpicture(in par_id_number text, in par_filename text) returns void as
$$
  update "Restaurantpicture"
    set filename = par_filename
    where respic_id = par_id_number;
$$
  language 'sql';


create function uploadrestaurantpicture(user_id text, filename text) returns void as
$$
  begin
    insert into "Restaurantpicture" values (respic_id, filename);
  end
$$
  language 'plpgsql';

--------------------------------------------------------------------------------------------------------------------

create function get_foodpicture(in par_id_number text, out text) returns text as
$$
  select filename
  from "Foodpicture"
  where foodpic_id = par_id_number;
$$
  language 'sql';


create function updatefoodpicture(in par_id_number text, in par_filename text) returns void as
$$
  update "Foodpicture"
    set filename = par_filename
    where foodpic_id = par_id_number;
$$
  language 'sql';


create function uploadfoodpicture(user_id text, filename text) returns void as
$$
  begin
    insert into "Foodpicture" values (foodpic_id, filename);
  end
$$
  language 'plpgsql';

--------------------------------------------------------------------------------------------------------------------


-- (1) Retrieve all users (GET)
create function list_users(out int, out text, out text, out text, out text, out text, out text, out text, out boolean) returns setof record as
$$
  select user_id, fname, lname, minitial, email, user_location, user_contact, password, is_active
  from "User";
$$
  language 'sql';


-- (2) Get a certain user (GET)
create function get_user(in par_user_id int, out text, out text, out text, out text, out text, out text, out text, out text, out boolean) returns setof record as
$$
  select user_id, fname, lname, minitial, email, user_location, user_contact, password, is_active
  from "User"
  where  user_id = par_user_id;
$$
  language 'sql';
  

-- (3) Add a new user (POST)
create function add_user(par_user_id int, par_fname text, par_lname text, par_minitial text, par_email text, par_user_location text, par_user_contact text, par_password text) returns void as
$body$
  begin
    insert into "User" values (par_user_id, par_fname, par_lname, par_minitial, par_email, par_user_location, par_user_contact, par_password, True);
  end
$body$
  language 'plpgsql';


-- (4) Update a certain user (UPDATE)
create function update_user(par_user_id int, par_fname text, par_lname text, par_minitial text, par_email text, par_user_location text, par_user_contact text, par_password text) returns void as
$$
  update "User"
  set fname = par_fname, lname = par_lname, minitial = par_minitial, email = par_email, user_location = par_user_location, user_contact, par_user_contact, password = par_password
  where  user_id = par_user_id;
$$
  language 'sql';


-- (5) Update a certain user by email(UPDATE)
create function update_user_email(par_user_id int, par_fname text, par_lname text, par_minitial text, par_email text, par_user_location text, par_user_contact text, par_password text) returns void as
$$
  update "User"
  set fname = par_fname, lname = par_lname, minitial = par_minitial, email = par_email, user_location = par_user_location, user_contact, par_user_contact, password = par_password
  where  email = par_email;
$$
  language 'sql';

  --------------------------------------------------------------------------------------------------------------------

-- (1) Retrieve all restaurant where is_active = True (GET)
create function list_restaurant(out int, out text, out text, out text, out text, out text, out boolean) returns setof record as
$$
  select restaurant_id, restaurant_name, restaurant_contact, restaurant_email, restaurant_address, restaurant_description, is_active
  from "Restaurant"
  where is_active = True;
$$
  language 'sql';

-- (2) Retrieve all restaurant in the DATABASE (GET)
create function list_restaurant_database(out int, out text, out text, out text, out text, out text, out boolean) returns setof record as
$$
  select restaurant_id, restaurant_name, restaurant_contact, restaurant_email, restaurant_address, restaurant_description, is_active
  from "Restaurant"
$$
  language 'sql';

  -- (3) Retrieve the restaurant with a certain starting with a certain string (GET)
create function get_restaurant_starting_with(in par_keyword text, out int, out text, out text, out text, out text, out text, out boolean) returns setof record as
$$
  select restaurant_id, restaurant_name, restaurant_contact, restaurant_email, restaurant_address, restaurant_description, is_active
  from "Restaurant"
  where lower(restaurant_name) Like par_keyword;
$$
  language 'sql';

   -- (4) Add restaurant (POST)
create function add_restaurant(par_restaurant_id int, par_restaurant_name text, par_restaurant_contact text, par_restaurant_email text, par_restaurant_address text, par_restaurant_description text) returns setof record as
$body$
  begin
    insert into "Restaurant" values (par_restaurant_id, par_restaurant_name, par_restaurant_contact, par_restaurant_email, par_restaurant_address, par_restaurant_description, True);
  end
$body$
  language 'sql';

-- (5) Update restaurant (UPDATE)
create function update_restaurant(par_restaurant_id int, par_restaurant_name text, par_restaurant_contact text, par_restaurant_email text, par_restaurant_address text, par_restaurant_description text) returns setof record as
$$
  update "Restaurant"
  set restaurant_name = par_restaurant_name, restaurant_contact = par_restaurant_contact, restaurant_email = par_restaurant_email, restaurant_address = par_restaurant_address, restaurant_description = par_restaurant_description, is_active = True
  where restaurant_id = par_restaurant_id;
$$
  language 'sql';

--(6) Delete restaurant (PUT)
create function delete_restaurant(in par_restaurant_id int) returns void as
$$
  update "Restaurant"
  set is_active = False
  where restaurant_id = par_restaurant_id;
$$
  language 'sql';


  --------------------------------------------------------------------------------------------------------------------

-- (1) Retrieve all food where is_active = True (GET)
create function list_food(out int, out text, out text, out real, out text, out boolean) returns setof record as
$$
  select food_id, restaurant_id, food_name, food_cost, food_description, is_active
  from "Food"
  where is_active = True;
$$
  language 'sql';

-- (2) Retrieve all food in the DATABASE (GET)
create function list_food_database(out int, out text, out text, out real, out text, out boolean) returns setof record as
$$
  select food_id, restaurant_id, food_name, food_cost, food_description, is_active
  from "Food"
$$
  language 'sql';

  -- (3) Retrieve the food with a certain starting with a certain string (GET)
create function get_food_starting_with(in par_keyword text, out int, out text, out text, out real, out text, out boolean) returns setof record as
$$
  select food_id, restaurant_id, food_name, food_cost, food_description, is_active
  from "Food"
  where lower(food_name) Like par_keyword;
$$
  language 'sql';

   -- (4) Add food (POST)
create function add_food(par_food_id int, par_restaurant_id int, par_food_name text, par_food_cost real, par_food_description text) returns setof record as
$body$
  begin
    insert into "Food" values (par_food_id, par_restaurant_id, par_food_name, par_food_cost, par_food_description, True);
  end
$body$
  language 'sql';

-- (5) Update food (UPDATE)
create function update_food(par_food_id int, par_restaurant_id int, par_food_name text, par_food_cost real, par_food_description text) returns setof record as
$$
  update "Food"
  set restaurant_id = par_restaurant_id, food_name = par_food_name, food_cost = par_food_cost, food_description = par_food_description, is_active = True
  where food_id = par_food_id;
$$
  language 'sql';

--(6) Delete restaurant (PUT)
create function delete_food(in par_food_id int) returns void as
$$
  update "Food"
  set is_active = False
  where food_id = par_food_id;
$$
  language 'sql';

  --------------------------------------------------------------------------------------------------------------------

-- (1) Retrieve all feedback of a particular restaurant (GET)
create function list_feedbackr_by_restaurant(in par_restaurant_id int, out feedbackr_id int, out restaurant_id int, out user_id text, out body text, out date_published timestamp) returns setof record as
$$
  select feedbackr_id, restaurant_id, user_id, body, date_published
  from "Feedbackr"
  where restaurant_id = par_restaurant_id and is_active = True;
$$
  language 'sql';  


-- (2) Retrieve all restaurant feedback on the database (GET)
create function list_feedbackr_database(out int, out int, out text, out text, out timestamp, out boolean) returns setof record as
$$
  select feedbackr_id, restaurant_id, user_id, body, date_published, is_active
  from "Feedbackr";
$$
  language 'sql'; 


-- (3) Retrieve all active feedbacks (GET)
create function list_feedbackr(out int, out int, out text, out text, out timestamp, out boolean) returns setof record as
$$
  select feedbackr_id, restaurant_id, user_id, body, date_published, is_active
  from "Feedbackr"
  where is_active = True;
$$
  language 'sql'; 


-- (4) Add a new feedback on a particular restaurant (POST)
create function add_feedbackr(par_feedbackr_id int, par_restaurant_id int, par_user_id text, par_body text) returns void as
$body$
  begin
    insert into "Feedbackr" values (par_feedbackr_id, par_restaurant_id, par_user_id, par_body, current_timestamp);
  end
$body$
  language 'plpgsql';


-- (5) Update (edit) an existing feedback (PUT) (You can only alter the body)
-- The timestamp will be modified also
create function edit_feedbackr(in par_feedbackr_id int, in par_body text) returns void as
$$
  update "Feedbackr"
  set body = par_body, date_published = current_timestamp
  where feedbackr_id = par_feedbackr_id;
$$
  language 'sql';

 
-- (6) Remove a feedback (PUT) (Set is_active = False)
create function delete_feedbackr(in par_feedbackr_id int) returns void as
$$
  update "Feedbackr"
  set is_active = False
  where feedbackr_id = par_feedbackr_id;
$$
  language 'sql';

  --------------------------------------------------------------------------------------------------------------------

-- (1) Retrieve all feedback of a particular food (GET)
create function list_feedbackf_by_food(in par_food_id int, out feedbackf_id int, out restaurant_id int, out user_id text, out body text, out date_published timestamp) returns setof record as
$$
  select feedbackf_id, food_id, user_id, body, date_published
  from "Feedbackr"
  where food_id = par_food_id and is_active = True;
$$
  language 'sql';  


-- (2) Retrieve all restaurant feedback on the database (GET)
create function list_feedbackf_database(out int, out int, out text, out text, out timestamp, out boolean) returns setof record as
$$
  select feedbackf_id, restaurant_id, user_id, body, date_published, is_active
  from "Feedbackf";
$$
  language 'sql'; 


-- (3) Retrieve all active feedbacks (GET)
create function list_feedbackf(out int, out int, out text, out text, out timestamp, out boolean) returns setof record as
$$
  select feedbackf_id, food_id, user_id, body, date_published, is_active
  from "Feedbackf"
  where is_active = True;
$$
  language 'sql'; 


-- (4) Add a new feedback on a particular restaurant (POST)
create function add_feedbackf(par_feedbackf_id int, par_food_id int, par_user_id text, par_body text) returns void as
$body$
  begin
    insert into "Feedbackf" values (par_feedbackf_id, par_food_id, par_user_id, par_body, current_timestamp);
  end
$body$
  language 'plpgsql';


-- (5) Update (edit) an existing feedback (PUT) (You can only alter the body)
-- The timestamp will be modified also
create function edit_feedbackf(in par_feedbackf_id int, in par_body text) returns void as
$$
  update "Feedbackf"
  set body = par_body, date_published = current_timestamp
  where feedbackf_id = par_feedbackf_id;
$$
  language 'sql';

 
-- (6) Remove a feedback (PUT) (Set is_active = False)
create function delete_feedbackf(in par_feedbackf_id int) returns void as
$$
  update "Feedbackf"
  set is_active = False
  where feedbackf_id = par_feedbackf_id;
$$
  language 'sql';

  --------------------------------------------------------------------------------------------------------------------

  -- (1) Retrieve all menuorder (GET)
  create function show_menuorder(out int, out text, out text, out int) returns setof record as
  $$
    select menuorder_id, food_id, restaurant_id, quantity
    from "Menuorder"
    where is_active = True;
  $$
    language 'sql';

--(2) Retrieve the menuorder which matches the menuorder id parameter (GET)
create function show_menuorder_by_id(in par_menuorder_id int, out int, out text, out text, out int) returns setof record as
$$
  select menuorder_id, food_id, restaurant_id, quantity
  from "Menuorder"
  where is_active = True and menuorder_id = par_menuorder_id;
$$
  language 'sql';

 --------------------------------------------------------------------------------------------------------------------

  -- (1) Retrieve all order (GET)
create function show_order(out int, out int, out int) returns setof record as
$$
  select order_id, user_id, menuorder_id
  from "Orders"
  where is_active = True;
$$
  language 'sql';


--(2) Retrieve the order which matches the order id parameter (GET)
create function show_order_by_id(in par_order_id int, out int, out int, out int) returns setof record as
$$
  select order_id, user_id, menuorder_id
  from "Orders"
  where is_active = True and order_id = par_order_id;
$$
  language 'sql';

-- (3) Add a new order (POST)
create function add_order(par_order_id int, par_user_id int, par_menuorder_id int) returns void as
$body$
  begin
    insert into "Orders" values (par_order_id, par_user_id, par_menuorder_id, True);
  end
$body$
  language 'plpgsql';


-- (5) Update food (UPDATE)
create function update_food(par_order_id int, par_user_id int, par_menuorder_id int) returns setof record as
$$
  update "Food"
  set user_id = par_user_id, menuorder_id = menuorder, is_active = True
  where order_id = par_order_id;
$$
  language 'sql';


 
-- (6) Remove order (PUT) (Set is_active = False)
create function delete_order(in par_order_id int) returns void as
$$
  update "Orders"
  set is_active = False
  where order_id = par_order_id;
$$
  language 'sql';


 --------------------------------------------------------------------------------------------------------------------


-- (1) Add transaction

create function add_transaction(par_foodtrans_id int, par_order_id int, par_total real) returns setof record as
$body$
  begin
    insert into "Foodtransaction" values (par_foodtrans_id, par_order_id, current_timestamp, par_total, True);
  end
$body$
  language 'plpgsql';

-- (2) Delete a transaction
-- This function only sets the is_active = False
create function delete_transaction(in par_foodtrans_id int) returns void as
$$
  update "Foodtransaction"
  set is_active = False
  where foodtrans_id = par_foodtrans_id;
$$
  language 'sql';

-- (3) Retrieve the transaction which matches the order id parameter (GET)
create function show_transaction_by_id(in par_foodtrans_id int, out int, out int, out real) returns setof record as
$$
  select foodtrans_id, order_id, total      
  from "Foodtransaction"
  where is_active = True and foodtrans_id = par_foodtrans_id;
$$
  language 'sql';