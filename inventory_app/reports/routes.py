from flask import request, render_template, redirect, url_for, Blueprint, flash
from flask_login import login_required, current_user

from inventory_app.app import db, check_admin
from inventory_app.products.models import Product
from inventory_app.categories.models import Category

products = Blueprint('reports', __name__, template_folder='templates', static_folder='static')
