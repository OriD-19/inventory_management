from flask import Blueprint, render_template, url_for, redirect
from flask_login import current_user, login_required

from inventory_app.app import db
from inventory_app.reports.generate_reports import generate_curr_inventory_volume, generate_graph_most_sold, generate_graph_most_bought
from inventory_app.transactions.models import TransactionHistory

import datetime

core = Blueprint('core', __name__, template_folder='templates', static_folder="static")

# main page needs to have the table of products, and a link to the detail of each product
@core.route('/')
def index():

    if not current_user.is_authenticated:
        return redirect(url_for('account.login'))

    graph1 = generate_graph_most_sold(db)
    graph2 = generate_graph_most_bought(db)
    graph3 = generate_curr_inventory_volume(db)

    transactions = TransactionHistory.query.order_by(TransactionHistory.time_registered.desc()).limit(10).all()

    all_transactions = TransactionHistory.query.all()
    curr_year = datetime.datetime.now().year
    curr_month = datetime.datetime.now().month
    curr_day = datetime.datetime.now().day
    month_transactions = TransactionHistory.query.filter(TransactionHistory.time_registered.between(datetime.datetime(curr_year, curr_month, 1), datetime.datetime(curr_year, curr_month, curr_day))).all()

    total_sales = [t.product_quantity * t.product.price for t in all_transactions if t.operation_type_id == 1]
    this_month_sales = [t.product_quantity * t.product.price for t in month_transactions if t.operation_type_id == 2]
    print(this_month_sales)

    return render_template('core/index.html', 
                           graphs=[graph1, graph2, graph3],
                           total_sales=sum(total_sales),
                           monthly_sales=sum(this_month_sales),
                           transactions=transactions)

@core.route('/create')
@login_required
def create():
    return render_template('core/create.html')

