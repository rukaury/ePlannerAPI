import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_swagger_ui import get_swaggerui_blueprint

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

# Create Swagger documentation blueprint.

swaggerui_blueprint = get_swaggerui_blueprint(
app.config['SWAGGER_URL'], 
app.config['SWAGGER_API_URL'],
config={'app_name': "ePlanner API"})

# Register blue prints
from app.auth.views import auth

app.register_blueprint(auth, url_prefix='/v1')

from app.events.views import events

app.register_blueprint(events, url_prefix='/v1')

from app.tickets.views import tickets

app.register_blueprint(tickets, url_prefix='/v1')

from app.guests.views import guests

app.register_blueprint(guests, url_prefix='/v1')

app.register_blueprint(swaggerui_blueprint, url_prefix='/docs')
