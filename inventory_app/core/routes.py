from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import current_user, login_required

from inventory_app.app import db, check_admin
from inventory_app.reports.generate_reports import generate_curr_inventory_volume, generate_graph_most_sold, generate_graph_most_bought
from inventory_app.transactions.models import TransactionHistory

import datetime

core = Blueprint('core', __name__, template_folder='templates', static_folder="static")

# main page needs to have the table of products, and a link to the detail of each product
@core.route('/')
@login_required
def index():

    graph1 = generate_graph_most_sold(db)
    graph2 = generate_graph_most_bought(db)
    graph3 = generate_curr_inventory_volume(db)

    transactions = TransactionHistory.query.order_by(TransactionHistory.time_registered.desc()).all()

    curr_year = datetime.datetime.now().year
    curr_month = datetime.datetime.now().month

    month_transactions = [t for t in transactions if t.time_registered <= datetime.datetime.now() and t.time_registered >= datetime.datetime(curr_year, curr_month, 1)]

    total_sales = [t.product_quantity * t.product.price for t in transactions if t.operation_type_id == 2]
    this_month_sales = [t.product_quantity * t.product.price for t in month_transactions if t.operation_type_id == 2]
    print(this_month_sales)

    return render_template('core/index.html', 
                           graphs=[graph1, graph2, graph3],
                           total_sales=sum(total_sales),
                           monthly_sales=sum(this_month_sales),
                           transactions=transactions[:10])

@core.route('/create')
@login_required
def create():

    if not check_admin(current_user):
        flash("No estas autorizado para ver esta página", "warning")
        return redirect(url_for('core.index'))

    return render_template('core/create.html')

