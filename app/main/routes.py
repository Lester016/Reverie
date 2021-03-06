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
    users = []
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
        # users = User.query.filter(User.id != current_user.id).order_by(
        #     func.random()).limit(3).all()
        tempUsers = User.query.filter(
            User.id != current_user.id).order_by(func.random()).all()

        for tempUser in tempUsers:
            if not current_user.is_following(tempUser) and len(users) <= 2:
                users.append(tempUser)

        return render_template('user-index.html', posts=posts, users=users, active='home')

    # posts = Post.query.order_by(Post.DatePosted.desc())
    return render_template('index.html', form=form)


@main.route("/profile/<string:email>")
def user_profile(email):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(Email=email).first_or_404()
    visitor = User.query.filter_by(Email=current_user.Email).first_or_404()
    posts = Post.query.filter_by(Author=user)\
        .order_by(Post.DatePosted.desc())\
        .paginate(page=page, per_page=5)

    followers = user.Followers.all()
    following = user.Followed.all()

    friends = []
    friendlists = []

    if len(followers) > len(following):
        for follower in followers:
            for followed in following:
                if (followed.id == follower.id):
                    friendlists.append(followed.id)
    else:
        for followed in following:
            for follower in followers:
                if (followed.id == follower.id):
                    friendlists.append(follower.id)

    visitorFollowers = visitor.Followers.all()
    visitorFollowing = visitor.Followed.all()

    visitorFriends = []
    visitorFriendlists = []

    if len(visitorFollowers) > len(visitorFollowing):
        for follower in visitorFollowers:
            for followed in visitorFollowing:
                if (followed.id == follower.id):
                    visitorFriendlists.append(followed.id)
    else:
        for followed in visitorFollowing:
            for follower in visitorFollowers:
                if (followed.id == follower.id):
                    visitorFriendlists.append(follower.id)

    # Compare if they have same friends using the user id's.
    mutuals = []

    if len(visitorFriendlists) > len(friendlists):
        for user1 in visitorFriendlists:
            for user2 in friendlists:
                if user1 == user2:
                    mutuals.append(user2)
    else:
        for user1 in friendlists:
            for user2 in visitorFriendlists:
                if user1 == user2:
                    mutuals.append(user2)

    for friendlist in friendlists:
        friends.append(User.query.filter_by(id=friendlist).first())

    return render_template('user-profile.html', posts=posts, user=user,
                           active=('profile' if user.Email ==
                                   current_user.Email else ''),
                           followers=followers, following=following, friends=friends,
                           friendlists=friendlists, visitorFriendlists=visitorFriendlists, mutuals=mutuals)


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
    visitor = User.query.filter_by(Email=current_user.Email).first_or_404()

    followers = user.Followers.all()
    following = user.Followed.all()

    friends = []
    friendlists = []

    if len(followers) > len(following):
        for follower in followers:
            for followed in following:
                if (followed.id == follower.id):
                    friendlists.append(followed.id)
    else:
        for followed in following:
            for follower in followers:
                if (followed.id == follower.id):
                    friendlists.append(follower.id)

    visitorFollowers = visitor.Followers.all()
    visitorFollowing = visitor.Followed.all()

    visitorFriends = []
    visitorFriendlists = []

    if len(visitorFollowers) > len(visitorFollowing):
        for follower in visitorFollowers:
            for followed in visitorFollowing:
                if (followed.id == follower.id):
                    visitorFriendlists.append(followed.id)
    else:
        for followed in visitorFollowing:
            for follower in visitorFollowers:
                if (followed.id == follower.id):
                    visitorFriendlists.append(follower.id)

    # Compare if they have same friends using the user id's.
    mutuals = []

    if len(visitorFriendlists) > len(friendlists):
        for user1 in visitorFriendlists:
            for user2 in friendlists:
                if user1 == user2:
                    mutuals.append(user2)
    else:
        for user1 in friendlists:
            for user2 in visitorFriendlists:
                if user1 == user2:
                    mutuals.append(user2)

    for friendlist in friendlists:
        friends.append(User.query.filter_by(id=friendlist).first())

    rendered = render_template(
        'pdf-template.html', friends=friends, posts=user.Posts, user=user, mutuals=mutuals, followers=followers)
    pdf = pdfkit.from_string(rendered, False)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

    return response


@main.route("/suggested-people")
def suggested_people():
    users = []
    tempUsers = User.query.filter(
        User.id != current_user.id).order_by(func.random()).all()

    for tempUser in tempUsers:
        if not current_user.is_following(tempUser):
            users.append(tempUser)
    return render_template('suggested-people.html', users=users, active='home')
