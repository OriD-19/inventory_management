from flask import request, render_template, redirect, url_for, Blueprint

from inventory_app.app import db
from inventory_app.products.models import Product
from inventory_app.categories.models import Category

products = Blueprint('products', __name__, template_folder='templates')

@products.route('/')
def index():
    products = Product.query.all()
    for product in products:
        print(product.category.category_name)
    return render_template('products/index.html', products=products)

@products.route('/<int:product_id>')
def detail(product_id):
    product = Product.query.get(product_id)
    return render_template('products/detail.html', product=product)

@products.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        product_name = request.form['product_name']
        stock = request.form['stock']
        description = request.form['description']
        img = request.form['img']
        category_id = request.form['category']

        new_product = Product(product_name=product_name, stock=stock, description=description, img=img, category_id=category_id)
        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('products.index'))
    
    categories = Category.query.all()
    return render_template('products/create.html', categories=categories)
