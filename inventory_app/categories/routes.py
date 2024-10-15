from flask import request, render_template, redirect, url_for, Blueprint

from inventory_app.app import db
from inventory_app.categories.models import Category

categories = Blueprint('categories', __name__, template_folder='templates')

@categories.route('/')
def index():
    categories = Category.query.all()
    return render_template('categories/index.html', categories=categories)

@categories.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        category = request.form['category']
        category = Category(category_name=category)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('categories.index'))

    return render_template('categories/create.html')