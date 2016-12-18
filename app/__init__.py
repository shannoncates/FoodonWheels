from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
app.debug = True


from app import views
