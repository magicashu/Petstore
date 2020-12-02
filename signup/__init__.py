from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
import random
import datetime
from functools import wraps
from werkzeug.utils import secure_filename
import os
from flask_mail import Mail, Message
from wtforms import Form


app = Flask(__name__)

app.config["MONGO_URI"] ="mongodb+srv://storedata:1234@ashupetstore.5j6ra.mongodb.net/storedata?retryWrites=true&w=majority"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'ashuujadhav2000@gmail.com'
app.config['MAIL_PASSWORD'] = 'ashuu123jadhav'

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

from signup import routes
