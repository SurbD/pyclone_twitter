from flask import Flask

from app.config import Config


def create_app(Config=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.main.routes import main
    from app.auth.routes import auth
    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app