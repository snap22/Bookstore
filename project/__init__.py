from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from project.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
#lm = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    #lm.init_app(app)

    from project.main.routes import main
    app.register_blueprint(main)


    with app.app_context():
        db.create_all()

    return app