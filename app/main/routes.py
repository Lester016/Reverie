from flask import (render_template, request, Blueprint,
                   redirect, url_for, flash, make_response)
from flask_login import (login_user, current_user, logout_user, login_required)
from app import db, bcrypt
from app.models import User, Post
from app.main.forms import RegistrationForm, SearchForm
from datetime import timedelta
from sqlalchemy.sql.expression import func
import pdfkit


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
        posts = current_user.followed_posts().all()
        users = User.query.filter(User.id != current_user.id).order_by(
            func.random()).limit(3).all()
        return render_template('user-index.html', posts=posts, users=users, active='home')

    posts = current_user.followed_posts().all()
    return render_template('index.html', form=form, posts=posts)


@main.route("/profile/<string:email>")
def user_profile(email):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(Email=email).first_or_404()
    posts = Post.query.filter_by(Author=user)\
        .order_by(Post.DatePosted.desc())\
        .paginate(page=page, per_page=5)

    followers = user.Followers.all()
    following = user.Followed.all()

    return render_template('user-profile.html', posts=posts, user=user,
                           active=('profile' if user.Email ==
                                   current_user.Email else ''),
                           followers=followers, following=following)


@main.route("/search", methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        inp = form.inp.data.lower()
        results = User.query.filter(User.Email.contains(inp))

        return render_template('search-list.html', results=results, form=form)

    return render_template('search-list.html', form=form)


@main.route("/profile/print-user-data/<string:email>")
def pdf_template(email):

    user = User.query.filter_by(Email=email).first()

    rendered = render_template('pdf-template.html',
                               firstname=user.FirstName, lastname=user.LastName, email=user.Email, posts=user.Posts)
    pdf = pdfkit.from_string(rendered, False)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

    return response
