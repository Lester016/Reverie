from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, BooleanField)
from wtforms.validators import (
    DataRequired, Length, Email, EqualTo, ValidationError)
from flask_login import current_user
from app.models import User


class RegistrationForm(FlaskForm):
    firstName = StringField('First Name', validators=[
        DataRequired(), Length(max=16)])
    lastName = StringField('Last Name', validators=[
                           DataRequired(), Length(max=16)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign up')

    # Function to make a custom error validation message
    def validate_username(self, field):
        user = User.query.filter_by(UserName=field.data).first()

        if user:
            raise ValidationError("Username is already taken.")

    def validate_email(self, field):
        user = User.query.filter_by(Email=field.data).first()

        if user:
            raise ValidationError("Email is already taken.")


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign in')
