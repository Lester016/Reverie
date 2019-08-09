from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, TextAreaField)
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed, FileField


class NewPost(FlaskForm):
    postImage = FileField('Add Image', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'])])
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')