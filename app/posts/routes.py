from flask import (render_template, url_for, flash,
                   redirect, request, Blueprint)
from app import db, bcrypt
from app.models import User
from app.posts.forms import NewPost
from datetime import timedelta

# The first argument is use to navigate different routes using that Blueprint
posts = Blueprint('posts', __name__)


@posts.route("/create_post", methods=['GET', 'POST'])
def create_post():
    form = NewPost()
    return render_template('posts/create-post.html', form=form)