from flask import request, render_template, redirect, url_for, Blueprint, flash
from flask_login import login_required, current_user

from inventory_app.app import db, check_admin
from inventory_app.products.models import Product
from inventory_app.categories.models import Category

products = Blueprint('products', __name__, template_folder='templates', static_folder="static")

@products.route('/')
@login_required
def index():
    products = Product.query.all()
    for product in products:
        print(product.category.category_name)
    return render_template('products/index.html', products=products)

@products.route('/<int:product_id>')
@login_required
def detail(product_id):
    product = Product.query.get(product_id)
    return render_template('products/detail.html', product=product)

@products.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if not check_admin(current_user):
        flash("No estas autorizado para ver esta página", "error")
        return redirect(url_for('products.index'))

    if request.method == 'POST':
        product_name = request.form['product_name']
        stock = request.form['stock']
        description = request.form['description']
        img = request.form['img']
        price = request.form['price']
        category_id = request.form['category']

        new_product = Product(product_name=product_name, stock=stock, description=description, price=price, img=img, category_id=category_id)
        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('products.index'))
    
    categories = Category.query.all()
    return render_template('products/create.html', categories=categories)
