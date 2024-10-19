from flask import request, render_template, redirect, url_for, Blueprint
from flask_login import login_required

from inventory_app.app import db
from inventory_app.transactions.models import TransactionHistory

transactions = Blueprint('transactions', __name__, template_folder='templates')

@transactions.route('/')
@login_required
def index():
    transactions = TransactionHistory.query.all()
    return render_template('transactions/index.html', transactions=transactions)

@transactions.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        transaction = TransactionHistory(
            product_id=request.form['product_id'],
            quantity=request.form['quantity'],
            operation_type_id=request.form['type']
        )
        db.session.add(transaction)
        db.session.commit()
        return redirect(url_for('transactions.index'))

    return render_template('transactions/new.html')
