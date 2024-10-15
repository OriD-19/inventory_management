from flask import request, render_template, redirect, url_for, Blueprint

from inventory_app.app import db
from inventory_app.transactions.models import Transaction

transactions = Blueprint('transactions', __name__, template_folder='templates')

@transactions.route('/')
def index():
    transactions = Transaction.query.all()
    return render_template('transactions/index.html', transactions=transactions)