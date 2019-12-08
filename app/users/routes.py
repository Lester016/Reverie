from flask import (render_template, url_for, flash,
                   redirect, request, Blueprint, make_response)
from flask_login import (login_user, current_user, logout_user, login_required)
from app import db, bcrypt
from app.models import User, Post
from app.users.forms import (RegistrationForm, LoginForm, ProfileUpdate,
                             RequestResetForm, ResetPasswordForm)
from app.users.utils import save_picture, send_reset_email
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
        user = User.query.filter_by(Email=form.email.data.lower()).first()
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

    followers = current_user.Followers.all()
    following = current_user.Followed.all()

    friends = []
    friendlists = []

    if len(followers) > len(following):
        for follower in followers:
            for followed in following:
                if (followed.id == follower.id):
                    friends.append(followed.id)
    else:
        for followed in following:
            for follower in followers:
                if (followed.id == follower.id):
                    friends.append(follower.id)

    for friend in friends:
        friendlists.append(User.query.filter_by(id=friend).first())

    return render_template('profile.html', title='Profile', posts=posts,
                           active='profile', followers=followers, following=following,
                           friends=friends, users=friendlists)


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
        flash('Successfully updated!', 'success')
        return redirect(url_for('users.profile'))
    elif request.method == 'GET':
        form.firstName.data = current_user.FirstName
        form.lastName.data = current_user.LastName
        form.email.data = current_user.Email
        form.profilePicture.data = current_user.ProfilePicture

    return render_template('profile-update.html', form=form, title='Profile Update', active='profile')


# Send a reset token to user email.
@users.route("/login/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(Email=form.email.data).first()
        # Call the function that will generate the email and token for the reset password.
        send_reset_email(user)
        flash("An email has been sent you can reset your email now.", 'success')
        return redirect(url_for('users.login'))
    return render_template('reset-request.html', title='Reset Password', form=form)


@users.route("/login/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid or expired token', 'danger')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('UTF-8')
        user.password = hashed_password
        db.session.commit()
        login_user(user, duration=timedelta)
        flash(f'Your password on {user.Email}, has been updated', 'success')
        return redirect(url_for('main.home'))
    return render_template('reset-token.html', title='Reset Password', form=form)


@users.route('/follow/<Email>')
@login_required
def follow(Email):
    user = User.query.filter_by(Email=Email).first()
    if user is None:
        flash('User {} not found.'.format(Email))
        return redirect(url_for('main.home'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('main.user_profile', email=user.Email))
    current_user.follow(user)
    db.session.commit()
    flash(f'You added {user.FirstName} {user.LastName}!', 'success')
    return redirect(url_for('main.user_profile', email=user.Email))


@users.route('/unfollow/<Email>')
@login_required
def unfollow(Email):
    user = User.query.filter_by(Email=Email).first()
    if user is None:
        flash('User {} not found.'.format(Email))
        return redirect(url_for('main.home'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('main.user_profile', email=user.Email))
    current_user.unfollow(user)
    db.session.commit()
    flash(f'You unfriend {user.FirstName} {user.LastName}!', 'danger')
    return redirect(url_for('main.user_profile', email=user.Email))

@users.route('/accept/<Email>')
@login_required
def accept(Email):
    user = User.query.filter_by(Email=Email).first()
    current_user.follow(user)
    db.session.commit()
    flash(f'You and {user.FirstName} {user.LastName} are now friends!', 'success')
    return redirect(url_for('main.user_profile', email=Email))

@users.route('/unfriend/<Email>')
@login_required
def unfriend(Email):
    user = User.query.filter_by(Email=Email).first()
    current_user.unfollow(user)
    db.session.commit()
    flash(f'You unfriend {user.FirstName} {user.LastName}!', 'danger')
    return redirect(url_for('users.profile'))

@users.route('/cancel/<Email>')
@login_required
def cancel(Email):
    user = User.query.filter_by(Email=Email).first()
    current_user.unfollow(user)
    db.session.commit()
    flash(f'You cancel your friend request to {user.FirstName} {user.LastName}!', 'danger')
    return redirect(url_for('users.profile'))