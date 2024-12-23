from flask import request, render_template, redirect, url_for, Blueprint
from flask_login import login_required

from inventory_app.app import db
from inventory_app.categories.models import Category

categories = Blueprint('categories', __name__, template_folder='templates', static_folder='static')

@categories.route('/')
@login_required
def index():
    categories = Category.query.all()
    return render_template('categories/index.html', categories=categories)

@categories.route('/products/<int:category_id>')
@login_required
def products_category(category_id):
    category = Category.query.get(category_id)
    products = category.products

    return render_template('categories/products_category.html', products=products, category=category)

@categories.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        category = request.form['category']
        category = Category(category_name=category)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('categories.index'))

    return render_template('categories/create.html')
