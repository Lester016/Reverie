from flask import (render_template, request,
                   Blueprint, redirect, url_for, flash)
from flask_login import (login_user, current_user, logout_user, login_required)
from app import db, bcrypt
from app.models import User, Post
from app.main.forms import RegistrationForm
from datetime import timedelta

main = Blueprint('main', __name__)


@main.route("/", methods=['GET', 'POST'])
def home():

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
        return redirect(url_for('main.home'))
    if current_user.is_authenticated:
        posts = Post.query.order_by(Post.DatePosted.desc())
        

        return render_template('user-index.html', posts=posts)

    posts = Post.query.order_by(Post.DatePosted.desc())
    return render_template('index.html', form=form, posts=posts)

@main.route("/profile/<string:email>")
def channel_post(email):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(email=email).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.datePosted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user-channel.html', posts=posts, user=user)