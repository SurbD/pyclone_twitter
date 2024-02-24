from datetime import datetime, timedelta, timezone

import jwt
from flask import current_app
from flask_login import UserMixin

from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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

    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return f"User('{self.username}', {self.email}', {self.image_file}')"

    def set_default_name(self):
        # print("Setting default name")
        if not self.name:
            self.name = self.username
            db.session.add(self)
            db.session.commit()

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


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"Post('{self.author.username}', {self.timestamp})"
