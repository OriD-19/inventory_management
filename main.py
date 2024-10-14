from dotenv import load_dotenv
from inventory_app.app import create_app
import sqlalchemy_libsql

load_dotenv()

flask_app = create_app()

def app(environ, start_response):
    return flask_app.wsgi_app(environ=environ, start_response=start_response)

if __name__ == '__main__':
    flask_app.run()