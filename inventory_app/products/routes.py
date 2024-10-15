from flask import request, render_template, redirect, url_for, Blueprint

from inventory_app.app import db
from inventory_app.products.models import Product

products = Blueprint('products', __name__, template_folder='templates')

@products.route('/')
def index():
    products = Product.query.all()
    return render_template('products/index.html', products=products)