from flask import (render_template, url_for, flash,
                   redirect, request, Blueprint)
from flask_login import (login_user, current_user, logout_user, login_required)
from app import db, bcrypt
from app.models import User, Post
from app.users.forms import RegistrationForm, LoginForm, ProfileUpdate
from app.users.utils import save_picture
from datetime import timedelta

# The first argument is use to navigate different routes using that Blueprint
users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        firstName = form.firstName.data.capitalize()
        lastName = form.lastName.data.capitalize()
        email = form.email.data.lower()
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('UTF-8')  # Encrypt the password stored in form.password.data
        user = User(FirstName=firstName, LastName=lastName,
                    Email=email, Password=hashed_password)
        db.session.add(user)
        db.session.commit()
        # Login the user with the session duration set
        login_user(user, duration=timedelta)
        # Second argument is optional, uses to assign what category the message is
        flash('Signed in!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form, title='Register')


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(Email=form.email.data).first()
        # If user exists decrypt the hashed_password
        if user and bcrypt.check_password_hash(user.Password, form.password.data):
            login_user(user, remember=form.remember.data,
                       duration=timedelta(minutes=15))
            flash('You have been logged in!', 'success')
            # When login.view is triggered the 'next' value is added to te url
            nextPage = request.args.get('next')
            return redirect(nextPage) if nextPage else redirect(url_for('main.home'))
        flash('Login Unsuccessful. Invalid Credentials', 'danger')
    return render_template('login.html', form=form, title="Sign in")


@users.route("/logout")
def logout():
    logout_user()  # Delete the session or the current_user data
    return redirect(url_for('users.login'))


@users.route("/profile")
@login_required
def profile():
    posts = Post.query.filter(Post.UserID.like(current_user.id)).order_by(
        (Post.DatePosted).desc()).all()
    return render_template('profile.html', title='Profile', posts=posts)


@users.route("/profile/update", methods=['GET', 'POST'])
@login_required
def profile_update():
    form = ProfileUpdate()
    if form.validate_on_submit():
        if form.profilePicture.data:
            pictureFile = save_picture(form.profilePicture.data)
            current_user.ProfilePicture = pictureFile
        current_user.FirstName = form.firstName.data.capitalize()
        current_user.LastName = form.lastName.data.capitalize()
        current_user.Email = form.email.data
        db.session.commit()
        flash('Successfully updated!')
        return redirect(url_for('users.profile'))
    elif request.method == 'GET':
        form.firstName.data = current_user.FirstName
        form.lastName.data = current_user.LastName
        form.email.data = current_user.Email
        form.profilePicture.data = current_user.ProfilePicture

    return render_template('profile-update.html', form=form, title='Profile Update')
