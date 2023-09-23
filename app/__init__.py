from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_bcrypt import Bcrypt

from app.config import config

db = SQLAlchemy()
mail = Mail()
bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)

    from app.main.routes import main
    from app.auth.routes import auth
    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app