from flask import Blueprint, render_template
from flask_login import current_user

from inventory_app.app import db

core = Blueprint('core', __name__, template_folder='templates')

# main page needs to have the table of products, and a link to the detail of each product
@core.route('/')
def index():
    return render_template('core/index.html', user=current_user)
