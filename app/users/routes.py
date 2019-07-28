from flask import (render_template, url_for, flash,
                   redirect, request, Blueprint)
from flask_login import (login_user, current_user, logout_user, login_required)
from app import db, bcrypt
from app.models import User
from app.users.forms import RegistrationForm, LoginForm
from datetime import timedelta

# The first argument is use to navigate different routes using that Blueprint
users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data.lower()
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('UTF-8') # Encrypt the password stored in form.password.data
        user = User(UserName=username, Email=email, Password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user, duration=timedelta) # Login the user with the session duration set
        flash('Signed in!', 'success') # Second argument is optional, uses to assign what category the message is
        return redirect(url_for('main.home'))
    return render_template('register.html', form=form, title='Register')


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(UserName=form.username.data).first()
        if user and bcrypt.check_password_hash(user.Password, form.password.data): # If user exists decrypt the hashed_password
            login_user(user, remember=form.remember.data,
                       duration=timedelta(minutes=15))
            flash('You have been logged in!', 'success')
            nextPage = request.args.get('next') # When login.view is triggered the 'next' value is added to te url
            return redirect(nextPage) if nextPage else redirect(url_for('main.home'))
        flash('Login Unsuccessful. Invalid Credentials', 'danger')
    return render_template('login.html', form=form, title="Sign in")


@users.route("/logout")
def logout():
    logout_user() # Delete the session or the current_user data
    return redirect(url_for('main.home'))
