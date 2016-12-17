from app import app
from flask import Flask, send_file



@app.route('/')
#@app.route('/index')
def index():
    return send_file("templates/index.html")
