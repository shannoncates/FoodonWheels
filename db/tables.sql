create table Users
(
	id				SERIAL8 PRIMARY KEY,
	first_name		VARCHAR(50),
	middle_initial	VARCHAR(50),
	last_name		VARCHAR(50),
	contact_number	VARCHAR(50),
	home_address	VARCHAR(50),
	email			VARCHAR(50),
	password		VARCHAR(50),
	is_active		BOOLEAN DEFAULT TRUE
);