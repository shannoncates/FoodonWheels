
create table "User"
(
  user_id int primary key,
  fname text,
  lname text,
  email text unique,
  user_location text,
  user_contact int,
  password text,
  awardpoints real default 0, 
  is_authenticated boolean default True,
  is_active boolean default True,
  is_anonymous boolean default True,
);

create table "Restaurant"
(
   restaurant_id primary key,
   restaurant_name text,
   is_active boolean default True
);

create table "Food"
(
   food_id primary key,
   food_name text,
   is_active boolean default True
)

create table "Categories"
(
  category_id int primary key,
  category_name text,
  is_active boolean default True
);

create table "Feedback"
(
  feedback_id int primary key,
  restaurant_id int references "Restaurant",
  food_id text references "Food",
  body text,
  date_published timestamp,
  is_active boolean default True
);

