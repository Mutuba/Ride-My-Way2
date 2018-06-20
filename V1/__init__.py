# services/users/project/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# instantiate the app
app = Flask(__name__, instance_relative_config=True)

# set config
#app_settings = os.getenv('APP_SETTINGS')
#app.config.from_object(app_settings)
app.config.from_object('config')


from V1.auth.views import auth_blueprint
app.register_blueprint(auth_blueprint)
from V1.ride.views import ride_blueprint
app.register_blueprint(ride_blueprint)
