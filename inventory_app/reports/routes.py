from flask import request, render_template, redirect, url_for, Blueprint, flash
from flask_login import login_required, current_user
from sqlalchemy.sql import text

from inventory_app.app import db, check_admin
from inventory_app.products.models import Product
from inventory_app.categories.models import Category

from inventory_app.reports.generate_reports import generate_graph_most_sold, generate_graph_most_bought

import pandas

reports = Blueprint('reports', __name__, template_folder='templates', static_folder='static')

@reports.route('/', methods=['GET'])
@login_required
def visualize_graph():

    graph1 = generate_graph_most_sold(db)
    graph2 = generate_graph_most_bought(db)

    a = text("""
            SELECT p.product_name, SUM(tr.product_quantity) 'Total de productos vendidos'
            FROM product p
            LEFT JOIN transaction_history tr
            ON tr.product_id = p.product_id
            WHERE tr.operation_type_id = 1 || tr.operation_type_id IS NULL
            GROUP BY p.product_name
            ORDER BY SUM(tr.product_quantity) DESC
            LIMIT 5;
    """)

    return f"""
        <img src='data:image/png;base64,{graph1}'/>
        <img src='data:image/png;base64,{graph2}'/>
        """
