from flask import (render_template, url_for, flash,
                   redirect, request, Blueprint)
from flask_login import current_user, login_required
from app import db
from app.models import Post
from app.posts.forms import NewPost
from app.posts.utils import save_post_image
from datetime import timedelta

# The first argument is use to navigate different routes using that Blueprint
posts = Blueprint('posts', __name__)


@posts.route("/create_post", methods=['GET', 'POST'])
@login_required
def create_post():
    form = NewPost()
    if form.validate_on_submit():
        postImage = ""
        if form.postImage.data:
            postImage = save_post_image(form.postImage.data)
        post = Post(
            Title=form.title.data,
            Content=form.content.data,
            ImageFile=postImage,
            Author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash("Succesfully Posted!")
        return redirect(url_for('users.profile'))

    return render_template('posts/create-post.html', form=form, title="Make a story")


@posts.route("/posts/<int:postID>", methods=['GET', 'POST'])
def post(postID):
    post = Post.query.get_or_404(postID)
    return render_template('posts/post.html', title="Posts", post=post)


@posts.route("/posts/<int:postID>/delete", methods=['POST'])
@login_required
def delete_post(postID):
    post = Post.query.get_or_404(postID)
    if post.Author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash("Post has been deleted", category='danger')
    return redirect(url_for('users.profile'))
