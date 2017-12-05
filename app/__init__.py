from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
from app import views