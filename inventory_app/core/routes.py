from flask import Blueprint, render_template, url_for, redirect
from flask_login import current_user

from inventory_app.app import db

core = Blueprint('core', __name__, template_folder='templates')

# main page needs to have the table of products, and a link to the detail of each product
@core.route('/')
def index():

    if not current_user.is_authenticated:
        return redirect(url_for('account.login'))

    return render_template('core/index.html', user=current_user)
