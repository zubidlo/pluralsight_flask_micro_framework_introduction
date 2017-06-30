
import os

from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

# configure database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = '\x93\x94!q\xdeV\xdcb\x93-\x81$@\xe2S\xd0\xa2\xbdw\xd9\xe6m$%'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'thermos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['DEBUG'] = False
db = SQLAlchemy(app)

# configure authentication
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)

import models
import views