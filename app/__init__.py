from flask_migrate import Migrate
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_seeder import FlaskSeeder
import os

login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URI"]
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    db.init_app(app)
    migrate.init_app(app, db)
    seeder = FlaskSeeder()
    seeder.init_app(app, db)

    from .hitmen import hitmen_bp
    app.register_blueprint(hitmen_bp)
    from .hits import hits_bp
    app.register_blueprint(hits_bp)
    from .auth import auth_bp
    app.register_blueprint(auth_bp)
    return app
