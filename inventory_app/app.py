from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///trial.db"

    db.init_app(app)

    from inventory_app.trial.routes import trial

    app.register_blueprint(trial, url_prefix='/trial')

    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()

    return app