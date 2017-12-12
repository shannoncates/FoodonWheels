
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
  is_active boolean default True,
  role text
);

create table "Restaurant"
(
   restaurant_id int primary key,
   restaurant_name text,
   restaurant_contact text,
   restaurant_email text,
   restaurant_address text,
   is_active boolean default True
);

create table "Food"
(
   food_id int primary key,
   restaurant_id text references "Restaurant",
   food_name text,
   food_cost text,
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
  food_id text references "Food"
  restaurant_id text references "Restaurant"
  quantity int
);

create table "Orders"
(
  order_id int primary key,
  user_id text references "User",
  menuorder_id references "Menuorder",
  is_active boolean default False
);

create table "Foodtransaction"
(
  foodtrans_id int primary key,
  order_id text references "Orders"
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
create function list_users(out int, out text, out text, out text, out text, out text, out text, out text, out boolean, out text) returns setof record as
$$
  select user_id, fname, lname, minitial, email, user_location, user_contact, password, is_active, role
  from "User";
$$
  language 'sql';


-- (2) Get a certain user (GET)
create function get_user(in par_user_id int, out text, out text, out text, out text, out text, out text, out text, out text, out boolean, out text) returns setof record as
$$
  select user_id, fname, lname, minitial, email, user_location, user_contact, password, is_active, role
  from "User"
  where  user_id = par_user_id;
$$
  language 'sql';
  

-- (3) Add a new user (POST)
create function add_user(par_user_id int, par_fname text, par_lname text, par_minitial text, par_email text, par_user_location text, par_user_contact text, par_passw text, par_role text) returns void as
$body$
  begin
    insert into "User" values (par_id_number, par_fname, par_lname, par_minitial, par_email, par_user_location, par_user_contact, par_passw, True, par_role);
  end
$body$
  language 'plpgsql';


-- (4) Update a certain user (UPDATE)
create function update_user(par_user_id int, par_fname text, par_lname text, par_minitial text, par_email text, par_user_location text, par_user_contact text, par_passw text, par_role text) returns void as
$$
  update "User"
  set fname = par_fname, lname = par_lname, minitial = par_minitial, email = par_email, user_location = par_user_location, user_contact, par_user_contact, password = par_passw, role=par_role
  where  user_id = par_user_id;
$$
  language 'sql';


-- (5) Update a certain user by email(UPDATE)
create function update_user_email(par_user_id int, par_fname text, par_lname text, par_minitial text, par_email text, par_user_location text, par_user_contact text, par_passw text, par_role text) returns void as
$$
  update "User"
  set fname = par_fname, lname = par_lname, minitial = par_minitial, email = par_email, user_location = par_user_location, user_contact, par_user_contact, password = par_passw, role=par_role
  where  email = par_email;
$$
  language 'sql';

  --------------------------------------------------------------------------------------------------------------------

-- (1) Retrieve all restaurant where is_active = True (GET)
create function list_restaurant(out int, out text, out text, out text, out text, out boolean) returns setof record as
$$
  select restaurant_id, restaurant_name, restaurant_contact, restaurant_email, restaurant_address, is_active
  from "Restaurant"
  where is_active = True;
$$
  language 'sql';

-- (2) Retrieve all restaurant in the DATABASE (GET)
create function list_restaurant_database(out int, out text, out text, out text, out text, out boolean) returns setof record as
$$
  select restaurant_id, restaurant_name, restaurant_contact, restaurant_email, restaurant_address, is_active
  from "Restaurant"
$$
  language 'sql';

  -- (3) Retrieve the restaurant with a certain starting with a certain string (GET)
create function get_restaurant_starting_with(in par_keyword text, out int, out text, out text, out text, out text, out boolean) returns setof record as
$$
  select restaurant_id, restaurant_name, restaurant_contact, restaurant_email, restaurant_address, is_active
  from "Restaurant"
  where lower(restaurant_name) Like par_keyword;
$$
  language 'sql';

   -- (4) Add restaurant (POST)
create function add_restaurant(par_restaurant_id int, par_restaurant_name text, par_restaurant_contact text, par_restaurant_email text, par_restaurant_address text) returns setof record as
$body$
  begin
    insert into "Restaurant" values (par_restaurant_id, par_restaurant_name, par_restaurant_contact, par_restaurant_email, par_restaurant_address, True);
  end
$body$
  language 'sql';

create function update_restaurant(par_restaurant_id int, par_restaurant_name text, par_restaurant_contact text, par_restaurant_email text, par_restaurant_address text) returns setof record as
$$
  update "Restaurant"
  set restaurant_name = par_restaurant_name, restaurant_contact = par_restaurant_contact, restaurant_email = par_restaurant_email, restaurant_address = par_restaurant_address, is_active = True
  where restaurant_id = par_restaurant_id;
$$
  language 'sql';

create function delete_restaurant(in par_thesis_id int) returns void as
$$
  update "Restaurant"
  set is_active = False
  where restaurant_id = par_restaurant_id;
$$
  language 'sql';