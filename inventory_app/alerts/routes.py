from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required

from inventory_app.app import db

from inventory_app.alerts.models import Alert

alerts = Blueprint('alerts', __name__, template_folder='templates')

@alerts.route('/')
@login_required
def index():

    alerts = Alert.query.all()
    return render_template('alerts/index.html', alerts=alerts)

@alerts.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    if request.method == 'POST':
        product_id = request.form['product_id']

        # use the username from the logged in user
        username = request.form['username']

        alert = Alert(product_id=product_id, username=username)
        db.session.add(alert)
        db.session.commit()

        flash(f"Alert for product {product_id} created by user {username}")
        return redirect(url_for('alerts.index'))

    return render_template('alerts/create.html')
