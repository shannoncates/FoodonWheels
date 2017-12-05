
DEBUG = True

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:cheche002@localhost/foodonwheels"
SQLALCHEMY_MIGRATION_REPO = os.path.join(basedir, 'db_repository')

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"