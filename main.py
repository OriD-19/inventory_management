from dotenv import load_dotenv
from inventory_app.app import create_app
import sqlalchemy_libsql

load_dotenv()

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)