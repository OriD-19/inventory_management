from flask import request, render_template, redirect, url_for, Blueprint, flash
from flask_login import login_required, current_user
from sqlalchemy.sql import text

from inventory_app.app import db, check_admin
from inventory_app.products.models import Product
import datetime

products = Blueprint('reports', __name__, template_folder='templates', static_folder='static')
from inventory_app.reports.generate_reports import generate_graph_most_sold, generate_graph_most_bought, generate_product_heatmap

reports = Blueprint('reports', __name__, template_folder='templates', static_folder='static')

@reports.route('/newReport', methods=['GET'])
@login_required
def new_report():

    products = Product.query.all()

    return render_template('reports/newReport.html', products=products)

@reports.route('/generatedReport', methods=['POST', 'GET'])
@login_required
def generated_report():

    if not check_admin(current_user):
        flash('No estas autorizado para ver esta página', "error")
        return redirect(url_for('products.list_products'))

    if not request.form['date']:
        flash('Por favor, ingresa una fecha', "error")
        return redirect(url_for('reports.new_report'))

    if not request.form['product_id']:
        flash('Por favor, ingresa un producto', "error")
        return redirect(url_for('reports.new_report'))

    # grab all the transactions for the product in the given date
    a = text("""
             SELECT tr.product_quantity, tr.operation_type_id
             FROM transaction_history tr 
             WHERE tr.product_id = :product_id AND tr.time_registered >= :date
             """)

    rs = db.session.execute(a, {'product_id': request.form['product_id'], 'date': request.form['date']})

    input_transactions = []
    output_transactions = []

    for row in rs:
        print(row)
        if row[1] == 1:
            input_transactions.append(row[0])
        else:
            output_transactions.append(row[0])

    product = Product.query.get(request.form['product_id'])
    graph = generate_product_heatmap(db, request.form['date'], request.form['product_id'])

    return render_template('reports/generatedReport.html', 
                           heatmap=graph, 
                           from_date=request.form['date'],
                           date_now=datetime.datetime.now().strftime('%Y-%m-%d'),
                           product=product, 
                           input_transactions=input_transactions, 
                           output_transactions=output_transactions)

