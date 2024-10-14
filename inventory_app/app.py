from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite+{os.getenv('TURSO_DATABASE_URL')}?authToken={os.getenv('TURSO_DATABASE_AUTH_TOKEN')}"

    db.init_app(app)

    from inventory_app.trial.routes import trial

    app.register_blueprint(trial, url_prefix='/trial')

    migrate = Migrate(app, db)

    return app