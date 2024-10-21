from flask import request, render_template, redirect, url_for, Blueprint
from flask_login import login_required

from inventory_app.app import db
from inventory_app.products.models import Product
from inventory_app.transactions.models import OperationType, TransactionHistory

transactions = Blueprint('transactions', __name__, template_folder='templates', static_folder='static')

@transactions.route('/in')
@login_required
def index_in():
    transactions = TransactionHistory.query.filter_by(operation_type_id=1).all()
    return render_template('transactions/index.html', transactions=transactions, out=False)

@transactions.route('/out')
@login_required
def index_out():
    transactions = TransactionHistory.query.filter_by(operation_type_id=2).all()
    return render_template('transactions/index.html', transactions=transactions, out=True)

@transactions.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        transaction = TransactionHistory(
            product_id=request.form['product_id'],
            product_quantity=request.form['product_quantity'],
            operation_type_id=request.form['operation_type_id']
        )
        db.session.add(transaction)
        db.session.commit()
        return redirect(url_for('transactions.index_in'))

    return render_template('transactions/create.html', products=Product.query.all(), transaction_types=OperationType.query.all())
