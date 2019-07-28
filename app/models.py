from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer # Use to generate token
from flask import current_app
from app import db, login_manager
from flask_login import UserMixin

# This is where the session or current_user gets the data when login_user is triggered
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(20), unique=True, nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    Password = db.Column(db.String(60), nullable=False)

    # Function to print the value of User model
    def __repr__(self):
        return f"User('{self.id}', '{self.UserName}', '{self.Email}', '{self.Password}')"