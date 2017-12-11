
create table "User"
(
  user_id text primary key,
  fname text,
  lname text,
  mname text,
  email text unique,
  user_location text,
  user_contact text,
  password text,
  awardpoints real default 0, 
  is_active boolean default True,
  role text
);

create table "Restaurant"
(
   restaurant_id text primary key,
   restaurant_name text,
   restaurant_contact text,
   restaurant_email text,
   restaurant_address text,
   is_active boolean default True
);

create table "Food"
(
   food_id text primary key,
   restaurant_id text references "Restaurant",
   food_name text,
   food_cost text,
   food_description text,
   is_active boolean default True
)

create table "Categories"
(
  category_id text primary key,
  category_name text,
  is_active boolean default True
);

create table "Feedbackr"
(
  feedbackr_id text primary key,
  restaurant_id text references "Restaurant",
  user_id text references "User",
  body text,
  date_published timestamp,
  is_active boolean default True
);

create table "Feedbackf"
(
  feedbackf_id text primary key,
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
  respic_id text primary key,
  filename text
);

create table "Menuorder"
(
  menuorder_id text primary key,
  food_id text references "Food"
  restaurant_id text references "Restaurant"
  quantity int
);

create table "Orders"
(
  order_id text primary key,
  user_id text references "User",
  menuorder_id references "Menuorder",
  is_active boolean default False
);

create table "Foodtransaction"
(
  foodtrans_id text primary key,
  order_id text references "Orders"
  foodtrans_date timestamp,
  total real,
  is_paid boolean default False
);
