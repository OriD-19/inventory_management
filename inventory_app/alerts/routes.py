from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from inventory_app.app import db

from inventory_app.alerts.models import Alert
from inventory_app.products.models import Product

from email.mime.text import MIMEText

alerts = Blueprint('alerts', __name__, template_folder='templates', static_folder='static')

@alerts.route('/')
@login_required
def index():

    alerts = Alert.query.all()
    return render_template('alerts/index.html', alerts=alerts)

@alerts.route('/create', methods=['POST', 'GET'])
@login_required
def create():

    if current_user.user_role.user_role != "admin":
        flash("You are not authorized to view this page.")
        return redirect(url_for('core.index'))

    if request.method == 'POST':
        product_id = request.form['product_id']

        min_product_stock = request.form['min_product_stock']

        alert = Alert(product_alert_id=product_id, user_alert_id=current_user.user_id, min_product_stock=min_product_stock)
        db.session.add(alert)
        db.session.commit()

        flash(f"Alert for product {product_id} created by user {current_user.username}")
        return redirect(url_for('alerts.index'))

    return render_template('alerts/create.html', products=Product.query.all())
