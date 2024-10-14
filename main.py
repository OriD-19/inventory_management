from dotenv import load_dotenv
from inventory_app.app import create_app
import sqlalchemy_libsql
import os

load_dotenv()

app = create_app()

if __name__ == '__main__':
    app.run(port=os.getenv("PORT"), debug=True)