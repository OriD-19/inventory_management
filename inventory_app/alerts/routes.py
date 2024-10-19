from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, user_unauthorized

from inventory_app.app import db

from inventory_app.alerts.models import Alert
from inventory_app.account.models import User
from inventory_app.products.models import Product

import smtplib
from email.mime.text import MIMEText
import os

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

        # use the username from the logged in user
        username = request.form['username']

        alert = Alert(product_id=product_id, username=username)
        db.session.add(alert)
        db.session.commit()

        flash(f"Alert for product {product_id} created by user {username}")
        return redirect(url_for('alerts.index'))

    return render_template('alerts/create.html', products=Product.query.all())

def send_email(from_user: User, to_user: User, product: Product):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    
    s.starttls()
    s.login(
        str(os.environ.get('GMAIL_ACCOUNT')), 
        str(os.environ.get('GMAIL_PASSWORD'))
    )

    alert_info = Alert.query.filter_by(user_id=to_user.user_id, product_id=product.product_id).first()

    """
    Reference: realpython.com
    As not all email clients display HTML content by default, and some people 
    choose only to receive plain-text emails for security reasons, it is 
    important to include a plain-text alternative for HTML messages.
    """

    text = f"""
            Hi, {to_user.username}!
            You have request this alert over the product {product.product_name}.
            The current stock for this product is {product.stock}.
            No longer want to receive this email? Contact with your administrator to remove this alert.
    """

    # the design of the email in HTML format
    HTML = """

    """
    HTMail = MIMEText(HTML, 'html')

    s.sendmail(from_email, to_email, "This is a test email")

    s.quit()

