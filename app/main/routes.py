from flask import (render_template, request, Blueprint)
from flask_login import (login_user, current_user, logout_user, login_required)
from app.users.forms import RegistrationForm
from app.models import User

main = Blueprint('main', __name__)

posts = [
    {
        'Title': 'Lorem Ipsum Dolor',
        'Author': 'John Doe',
        'TimeRead': '5 min',
        'Content': 'We spend a lot of time advising startups. Though one-on-one advice will always be crucial',
    },
    {
        'Title': 'Lorem Ipsum Dolor',
        'Author': 'John Doe',
        'TimeRead': '5 min',
        'Content': 'We spend a lot of time advising startups. Though one-on-one advice will always be crucial',
    },
    {
        'Title': 'Lorem Ipsum Dolor',
        'Author': 'John Doe',
        'TimeRead': '5 min',
        'Content': 'We spend a lot of time advising startups. Though one-on-one advice will always be crucial',
    },
    {
        'Title': 'Lorem Ipsum Dolor',
        'Author': 'John Doe',
        'TimeRead': '5 min',
        'Content': 'We spend a lot of time advising startups. Though one-on-one advice will always be crucial',
    },
    {
        'Title': 'Lorem Ipsum Dolor',
        'Author': 'John Doe',
        'TimeRead': '5 min',
        'Content': 'We spend a lot of time advising startups. Though one-on-one advice will always be crucial',
    },
    {
        'Title': 'Lorem Ipsum Dolor',
        'Author': 'John Doe',
        'TimeRead': '5 min',
        'Content': 'We spend a lot of time advising startups. Though one-on-one advice will always be crucial',
    },
    {
        'Title': 'Lorem Ipsum Dolor',
        'Author': 'John Doe',
        'TimeRead': '5 min',
        'Content': 'We spend a lot of time advising startups. Though one-on-one advice will always be crucial',
    },
    {
        'Title': 'Lorem Ipsum Dolor',
        'Author': 'John Doe',
        'TimeRead': '5 min',
        'Content': 'We spend a lot of time advising startups. Though one-on-one advice will always be crucial',
    }
]


@main.route("/", methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        return render_template('user-index.html', posts=posts)
    
    return render_template('index.html', posts=posts, form=form)


@main.route("/profile")
def profile():
    return render_template('profile.html', posts=posts)
