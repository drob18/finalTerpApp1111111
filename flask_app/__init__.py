# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_talisman import Talisman
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

# stdlib
from datetime import datetime
import os

# local
from .client import MovieClient


db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()
movie_client = MovieClient("49788269")

from .users.routes import users
from .movies.routes import movies


def page_not_found(e):
    return render_template("404.html"), 404


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_pyfile("config.py", silent=False)
    if test_config is not None:
        app.config.update(test_config)
    
    csp = {
        'default-src': ['\'self\'',
        'cdnjs.cloudflare.com',
        'stackpath.bootstrapcdn.com',
        'code.jquery.com',
        'cdn.jsdelivr.net',
        '\'unsafe-inline\''
        ],
        'media-src': '*',
        'img-src': '*'
    }
    Talisman(app,content_security_policy=csp)
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(users)
    app.register_blueprint(movies)
    app.register_error_handler(404, page_not_found)

    login_manager.login_view = "users.login"

    return app