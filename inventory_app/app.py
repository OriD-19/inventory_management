from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from google.cloud.sql.connector import Connector, IPTypes

db = SQLAlchemy()
connector = Connector()
bcrypt = Bcrypt()

def get_connection():
    conn = connector.connect(
        str(os.environ.get("INSTANCE_CONNECTION_NAME")),
        "pymysql",
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASS"),
        db=os.environ.get("DB_NAME"),
        ip_type=IPTypes.PUBLIC,
    )

    return conn

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "creator": get_connection,
    }

    # will use an env variable, but probably a randomly generated key would be better...
    app.secret_key = os.environ.get("SECRET_KEY") or 'asdflkj32l4j12klj3kljasdflkj'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader

    def load_user(user_id):
        from inventory_app.account.models import User

        return User.query.get(user_id)

    bcrypt.init_app(app)

    # import all the blueprints and register them
    from inventory_app.transactions.routes import transactions
    from inventory_app.categories.routes import categories
    from inventory_app.products.routes import products
    from inventory_app.account.routes import account
    from inventory_app.alerts.routes import alerts
    from inventory_app.core.routes import core

    app.register_blueprint(products, url_prefix='/products')
    app.register_blueprint(transactions, url_prefix='/transactions')
    app.register_blueprint(categories, url_prefix='/categories')
    app.register_blueprint(account, url_prefix='/account')
    app.register_blueprint(alerts, url_prefix='/alerts')
    app.register_blueprint(core, url_prefix='/')


    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()

    return app
