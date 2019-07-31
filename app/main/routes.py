from flask import (render_template, request, Blueprint)

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


@main.route("/")
def home():
    return render_template('index.html', posts=posts)
