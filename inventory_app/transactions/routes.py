from email.mime.nonmultipart import MIMENonMultipart
from flask import flash, request, render_template, redirect, url_for, Blueprint
from flask_login import login_required

from inventory_app.app import db
from inventory_app.products.models import Product
from inventory_app.alerts.models import Alert
from inventory_app.transactions.models import OperationType, TransactionHistory

from datetime import datetime
import smtplib
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart
import os

transactions = Blueprint('transactions', __name__, template_folder='templates', static_folder='static')

"""
Sending emails, kind of a pain, but is necessary...
"""
def send_email(from_email, to_user, product):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    
    s.starttls()

    s.login(
        str(os.environ.get('GMAIL_ACCOUNT')), 
        str(os.environ.get('GMAIL_PASS'))
    )

    message = MIMEMultipart("alternative")
    message["Subject"] = "Alerta de stock para producto " + product.product_name
    message["From"] = from_email
    message["To"] = to_user.email

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
    HTML = f"""
        <h1>Hi, {to_user.username}!</h1>
        <p>You have requested this alert over the product {product.product_name}.</p>
        <p>The current stock for this product is {product.stock}.</p>
        <p>No longer want to receive this email? Contact with your administrator to remove this alert.</p>

    """
    text_mail = MIMEText(text, 'plain')
    HTMail = MIMEText(HTML, 'html')

    message.attach(HTMail)
    message.attach(text_mail)

    try:
        errs = s.sendmail(from_email, to_user.email, message.as_string())
    except:
        return False

    s.quit()
    return True


def check_send_alert(product):
    alerts_attached = product.alerts

    for alert in alerts_attached:
        if product.stock <= alert.min_product_stock:
            # send email to the user in the alert
            user = alert.user

            # we'll be using my email to write these things, just cuz

            res = send_email(str(os.environ.get('GMAIL_ACCOUNT')), user, product)            

            if not res:
                flash("Error al enviar el correo, revisa la configuración de tu cuenta de correo", "error")

def validate_transaction_form(form):
    validForm = True
    errors = {}
    if not form['product_quantity'].isnumeric() or int(form['product_quantity']) < 1:
        errors['quant'] = "Cantidad inválida"

    if not form['product_id'].isnumeric() or not Product.query.get(form['product_id']):
        errors['product'] = 'Producto inválido'

    date_time = datetime.now()
    try:
        if not form["fecha"] == "":
            date_time = datetime.strptime(form['fecha'], '%Y-%m-%d').date()
    except ValueError:
        errors['date'] = 'Formato de fecha inválido'

    return errors, date_time

@transactions.route('/in')
@login_required
def index_in():
    transactions = TransactionHistory.query.filter_by(operation_type_id=1).all()
    products = Product.query.all()
    return render_template('transactions/index.html', products=products, transactions=transactions, out=False)

@transactions.route('/out')
@login_required
def index_out():
    transactions = TransactionHistory.query.filter_by(operation_type_id=2).all()
    products = Product.query.all()
    return render_template('transactions/index.html', products=products, transactions=transactions, out=True)

@transactions.route('/in/product/<int:id>', methods=['GET'])
@login_required
def show_in(id):
    transactions = TransactionHistory.query.filter_by(product_id=id, operation_type_id=1).order_by(TransactionHistory.time_registered.desc()).all()
    product = Product.query.get(id)
    return render_template('transactions/show.html', product=product, transactions=transactions, out=False)

@transactions.route('/out/product/<int:id>', methods=['GET'])
@login_required
def show_out(id):
    transactions = TransactionHistory.query.filter_by(product_id=id, operation_type_id=2).order_by(TransactionHistory.time_registered.desc()).all()
    product = Product.query.get(id)
    return render_template('transactions/show.html', product=product, transactions=transactions, out=True)

@transactions.route('/create/in', methods=['GET', 'POST'])
@login_required
def create_in():
    if request.method == 'POST':

        errors, date_time = validate_transaction_form(request.form)

        if not len(dict.keys(errors)) == 0:
            return render_template('transactions/entrada.html', errors=errors)

        transaction = TransactionHistory(
            product_id=request.form['product_id'],
            product_quantity=request.form['product_quantity'],
            operation_type_id=1,
            time_registered=date_time
        )
        db.session.add(transaction)
        db.session.commit()

        flash('Transacción registrada exitosamente', 'success')
        return redirect(url_for('transactions.index_in'))

    return render_template('transactions/entrada.html', products=Product.query.all(), errors={})

@transactions.route('/create/out', methods=['GET', 'POST'])
@login_required
async def create_out():
    if request.method == 'POST':

        errors, date_time = validate_transaction_form(request.form)

        if not len(dict.keys(errors)) == 0:
            return render_template('transactions/entrada.html', errors=errors)

        transaction = TransactionHistory(
            product_id=request.form['product_id'],
            product_quantity=request.form['product_quantity'],
            operation_type_id=2,
            time_registered=date_time
        )

        db.session.add(transaction)
        db.session.commit()

        product = Product.query.get(request.form['product_id'])

        check_send_alert(product)

        flash('Transacción registrada exitosamente', 'success')
        return redirect(url_for('transactions.index_out'))

    return render_template('transactions/salida.html', products=Product.query.all(), errors={})

