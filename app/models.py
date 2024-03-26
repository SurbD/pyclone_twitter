import jwt
from flask import current_app, request
from flask_login import UserMixin

from datetime import datetime, timedelta, timezone
import hashlib

from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Follow(db.Model):
    __tablename__ = "follows"
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    date_of_birth = db.Column(db.DateTime())
    confirmed = db.Column(db.Boolean, default=False)

    name = db.Column(db.String(64), nullable=True)
    location = db.Column(db.String(64), nullable=True, default="Earth-X 2.0")
    about_me = db.Column(db.Text(), nullable=True)
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar_hash = db.Column(db.String(32))

    posts = db.relationship('Post', backref='author', lazy='dynamic')
    # TODO: read the sqlalchemy documentation on database relationship and postgressql relationship.
    followed = db.relationship('Follow',
                               foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    followers = db.relationship('Follow',
                               foreign_keys=[Follow.followed_id],
                               backref=db.backref('followed', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')

    def __repr__(self):
        return f"User('{self.username}', {self.email}', {self.image_file}')"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = self.gravatar()

    def set_default_name(self):
        # print("Setting default name")
        if not self.name:
            self.name = self.username
            db.session.add(self)
            db.session.commit()

    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'https://www.gravatar.com/avatar'

        hash = self.avatar_hash or self.gravatar_hash()
        return f'{url}/{hash}?s={size}&d={default}&r={rating}'

    def change_email(self, token):
        pass

    def ping(self):
        self.set_default_name()
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def get_token(self, expiration=600):
        token = jwt.encode(
            {
                "user_id": self.id,
                "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=expiration),
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )

        return token

    @staticmethod
    def confirm_token(token):
        try:
            data = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                leeway=timedelta(seconds=10),
                algorithms=["HS256"],
            )
        except:
            return None

        if not (user_id := data.get("user_id")):
            return None
        return User.query.get(user_id)
    
    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)
    
    def is_following(self, user):
        if user.id is None:
            return False
        return self.followed.filter_by(followed_id=user.id).first() is not None
    
    def is_followed_by(self, user):
        if user.id is None:
            return False
        return self.followers.filter_by(follower_id=user.id).first() is not None


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"Post('{self.author.username}', {self.timestamp})"

