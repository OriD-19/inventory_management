from flask import Blueprint, render_template, url_for, redirect
from flask_login import current_user, login_required

from inventory_app.app import db
from inventory_app.reports.generate_reports import generate_curr_inventory_volume, generate_graph_most_sold, generate_graph_most_bought

core = Blueprint('core', __name__, template_folder='templates', static_folder="static")

# main page needs to have the table of products, and a link to the detail of each product
@core.route('/')
def index():

    if not current_user.is_authenticated:
        return redirect(url_for('account.login'))

    graph1 = generate_graph_most_sold(db)
    graph2 = generate_graph_most_bought(db)
    graph3 = generate_curr_inventory_volume(db)

    return render_template('core/index.html', graphs=[graph1, graph2, graph3])

@core.route('/create')
@login_required
def create():
    return render_template('core/create.html')

