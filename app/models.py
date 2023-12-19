from datetime import datetime, timedelta, timezone
from flask import current_app
from flask_login import UserMixin
from app import db, login_manager
import jwt


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    date_of_birth = db.Column(db.DateTime())
    confirmed = db.Column(db.Boolean, default=False)

    name = db.Column(db.String(64), nullable=True)
    location = db.Column(db.String(64), nullable=True)
    about_me = db.Column(db.Text(), nullable=True)
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.username}', {self.email}', {self.image_file}')"

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def get_token(self, expiration=600):

        token = jwt.encode(
            {
                'user_id': self.id,
                'exp': datetime.now(tz=timezone.utc) + timedelta(seconds=expiration)
            },
            current_app.config['SECRET_KEY'],
            algorithm="HS256"
        )

        return token
    
    @staticmethod
    def confirm_token(token):
        try:
            data = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                leeway= timedelta(seconds=10),
                algorithms=["HS256"]
            )
        except:
            return None
        
        if not (user_id := data.get('user_id')):
            return None
        return User.query.get(user_id)
    
