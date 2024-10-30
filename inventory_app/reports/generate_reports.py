import base64
from io import BytesIO
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import matplotlib

from sqlalchemy.sql import text
import pandas

matplotlib.use('agg')
sns.set_theme()
sns.set(rc={'figure.figsize':(10,5),})

def generate_graph_most_bought(db):
    a = text("""
            SELECT p.product_name, SUM(tr.product_quantity) 'Total de productos comprados'
            FROM product p
            LEFT JOIN transaction_history tr
            ON tr.product_id = p.product_id
            WHERE tr.operation_type_id = 1 || tr.operation_type_id IS NULL
            GROUP BY p.product_name
            ORDER BY SUM(tr.product_quantity) DESC
            LIMIT 5;
    """)

    rs = db.session.execute(a)

    product_list = []
    product_quantity = []

    for row in rs:
        product_list.append(row[0])
        if not row[1] is None:
            product_quantity.append(row[1])
        else:
            product_quantity.append(0)


    df = pandas.DataFrame({
        "product_list": product_list,
        "product_quantity": product_quantity
    })
    print(df)

    g = sns.barplot(data=df, x="product_list", y="product_quantity")
    g.set(xlabel="Productos", ylabel="Compras (Entradas)")

    g.bar_label(g.containers[0])
    g.set_title("Top 5 productos más comprados")

    buf = BytesIO()
    g.figure.savefig(buf, format="png")

    data = base64.b64encode(buf.getbuffer()).decode("utf-8")
    buf.flush()
    buf.close()

    g.figure.clear()

    return data

def generate_graph_most_sold(db):
    a = text("""
            SELECT p.product_name, SUM(tr.product_quantity) 'Total de productos vendidos'
            FROM product p
            LEFT JOIN transaction_history tr
            ON tr.product_id = p.product_id
            WHERE tr.operation_type_id = 2 || tr.operation_type_id IS NULL
            GROUP BY p.product_name
            ORDER BY SUM(tr.product_quantity) DESC
            LIMIT 5;
    """)

    rs = db.session.execute(a)

    product_list = []
    product_quantity = []

    for row in rs:
        product_list.append(row[0])
        if not row[1] is None:
            product_quantity.append(row[1])
        else:
            product_quantity.append(0)


    df = pandas.DataFrame({
        "product_list": product_list,
        "product_quantity": product_quantity
    })
    print(df)

    g = sns.barplot(data=df, x="product_list", y="product_quantity")
    g.set(xlabel="Productos", ylabel="Ventas (Salidas)")

    g.bar_label(g.containers[0])
    g.set_title("Top 5 productos más vendidos")

    buf = BytesIO()
    g.figure.savefig(buf, format="png")

    data = base64.b64encode(buf.getbuffer()).decode("utf-8")
    buf.flush()
    buf.close()

    g.figure.clear()

    return data
    

def generate_curr_inventory_volume(db):

    a = text("""
        SELECT p.product_name, p.stock
        FROM product p
        ORDER BY p.stock DESC;
    """)

    rs = db.session.execute(a)

    product_list = []
    product_quantity = []

    for row in rs:
        product_list.append(row[0])
        if not row[1] is None:
            product_quantity.append(row[1])
        else:
            product_quantity.append(0)


    df = pandas.DataFrame({
        "product_list": product_list,
        "product_quantity": product_quantity
    })

    total_stock = df.product_quantity.sum()

    # grab the top 5 products with most stock
    df2 = df[:5].copy()

    other_values = pandas.DataFrame({
        'product_list': ['Otros'],
        'product_quantity': [total_stock - df2.product_quantity.sum()]
    })

    if other_values.product_quantity[0] > 0:
        df2 = pandas.concat([df2, other_values])

    fig, ax = plt.subplots()
    ax.pie(df2.product_quantity, labels=df2.product_list, autopct='%1.1f%%')

    buf = BytesIO()
    fig.savefig(buf, format="png")

    data = base64.b64encode(buf.getbuffer()).decode("utf-8")

    buf.flush()
    buf.close()

    fig.clear()

    return data

