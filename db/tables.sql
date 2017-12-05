
create table "User"
(
  first_name text primary key,
  last_name text,
  middle_initial text,
  email text unique,
  password text,
  is_authenticated boolean default True,
  is_active boolean default True,
  is_anonymous boolean default True,
  role text
);

