from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from inventory_app.app import db, check_admin

from inventory_app.alerts.models import Alert
from inventory_app.products.models import Product
from inventory_app.account.models import User

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

    if not check_admin(current_user):
        flash("No estas autorizado para ver esta página", "warning")
        return redirect(url_for('alerts.index'))

    if request.method == 'POST':
        product_id = request.form['product_id']
        min_product_stock = request.form['min_product_stock']
        user_id = request.form['user_id']

        alert = Alert(product_alert_id=product_id, user_alert_id=user_id, min_product_stock=min_product_stock)
        db.session.add(alert)
        db.session.commit()

        flash(f"Alerta para producto {product_id} creada por usuario {current_user.username}", "success")
        return redirect(url_for('alerts.index'))

    users = User.query.all()
    return render_template('alerts/create.html', products=Product.query.all(), users=users)
