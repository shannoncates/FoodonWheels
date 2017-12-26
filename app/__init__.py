from flask import Flask, render_template, jsonify, request
#from flask_sqlalchemy import SQALchemy

app = Flask(__name__)
app.config.from_pyfile("config.py")
#db = SQALchemy(app)

from app import views