from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

from google.cloud.sql.connector import Connector, IPTypes

db = SQLAlchemy()
connector = Connector()

def get_connection():
    conn = connector.connect(
        os.environ.get("INSTANCE_CONNECTION_NAME"),
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

    db.init_app(app)

    # import all the blueprints and register them
    from inventory_app.transactions.routes import transactions
    from inventory_app.categories.routes import categories
    from inventory_app.products.routes import products

    app.register_blueprint(products, url_prefix='/products')
    app.register_blueprint(transactions, url_prefix='/transactions')
    app.register_blueprint(categories, url_prefix='/categories')


    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()

    return app