import os
# Installable
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config

# Libraries Initialization
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

# Assign a route where the login view redirect to.
login_manager.login_view = 'users.login'

mail = Mail()


# App factory
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)  # Mapped the configurations

    # Initialize flask app inside these libraries instance.
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from app.main.routes import main
    from app.users.routes import users
    from app.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(errors)

    return app

# This is for initializing a db
# x = create_app()
# x.app_context().push()
