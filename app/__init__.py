import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Initialize application
app = Flask(__name__, static_folder=None)

# app configuration
app_settings = os.getenv(
    'APP_SETTINGS',
    'app.config.DevelopmentConfig'
)

app.config.from_object(app_settings)

# Initialize Bcrypt
bcrypt = Bcrypt(app)

# Initialize Flask Sql Alchemy
db = SQLAlchemy(app)

# Register blue prints
from app.auth.views import auth

app.register_blueprint(auth, url_prefix='/v1')

from app.events.views import events

app.register_blueprint(events, url_prefix='/v1')

from app.tickets.views import tickets

app.register_blueprint(tickets, url_prefix='/v1')

from app.guests.views import guests

app.register_blueprint(guests, url_prefix='/v1')

from app.docs.views import docs

app.register_blueprint(docs)