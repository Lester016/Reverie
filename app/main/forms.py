from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, BooleanField)
from wtforms.validators import (
    DataRequired, Length, Email, EqualTo, ValidationError)
from app.models import User


class RegistrationForm(FlaskForm):
    firstName = StringField('First Name', validators=[
        DataRequired(), Length(max=16)])
    lastName = StringField('Last Name', validators=[
                           DataRequired(), Length(max=16)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password', validators=[
                                    DataRequired(), EqualTo('password')])
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


class SearchForm(FlaskForm):
    inp = StringField('Search Email...', validators=[
        DataRequired(), Email()] )
