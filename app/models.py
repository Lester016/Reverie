from datetime import datetime
# Use to generate token
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from app import db, login_manager
from flask_login import UserMixin

# This is where the session or current_user gets the data when login_user is triggered
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


Followers = db.Table('followers',
                     db.Column('follower_id', db.Integer,
                               db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer,
                               db.ForeignKey('user.id'))
                     )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(20), nullable=False)
    LastName = db.Column(db.String(20), nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    Password = db.Column(db.String(60), nullable=False)
    ProfilePicture = db.Column(db.String(20), nullable=False,
                               default='default.png')
    Posts = db.relationship('Post', backref='Author', lazy=True)
    Followed = db.relationship(
        'User', secondary=Followers,
        primaryjoin=(Followers.c.follower_id == id),
        secondaryjoin=(Followers.c.followed_id == id),
        backref=db.backref('Followers', lazy='dynamic'), lazy='dynamic')

    # Generate a reset token in the s.dumps with SECRET_KEY as secret_key argument in Serializer.

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        # Store the token into SECRET_KEY.
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        # Get the token stored in SECRET_KEY.
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            # Load or Decrypt the token stored in SECRET_KEY.
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    # Function to print the value of User model

    def __repr__(self):
        return f"User('{self.FirstName}', '{self.LastName}', '{self.Email}', '{self.ProfilePicture}')"

    def follow(self, user):
        if not self.is_following(user):
            self.Followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.Followed.remove(user)

    def is_following(self, user):
        return self.Followed.filter(
            Followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        Followed = Post.query.join(
            Followers, (Followers.c.followed_id == Post.UserID)).filter(
                Followers.c.follower_id == self.id)
        own = Post.query.filter_by(UserID=self.id)
        return Followed.union(own).order_by(Post.DatePosted.desc())

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(100), nullable=False)
    ImageFile = db.Column(db.String(20))
    DatePosted = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    Content = db.Column(db.Text, nullable=False)
    UserID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.Title}', '{self.DatePosted}')"
