from flask import Blueprint, render_template, url_for, redirect
from flask_login import current_user, login_required

from inventory_app.app import db

core = Blueprint('core', __name__, template_folder='templates', static_folder="static")

# main page needs to have the table of products, and a link to the detail of each product
@core.route('/')
def index():

    if not current_user.is_authenticated:
        return redirect(url_for('account.login'))

    return render_template('core/index.html')

@core.route('/create')
@login_required
def create():
    return render_template('core/create.html')

