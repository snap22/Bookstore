from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from project.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "account.login"
login_manager.login_message_category = "info"
login_manager.login_message = "Najprv sa musíte prihlásiť"

def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from project.main.routes import main
    from project.users.account.routes import account
    from project.users.admin.routes import admin
    app.register_blueprint(main)
    app.register_blueprint(account)
    app.register_blueprint(admin)


    with app.app_context():
        db.create_all()

    return app