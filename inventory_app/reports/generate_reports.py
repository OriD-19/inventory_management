import base64 
from io import BytesIO
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import matplotlib

from sqlalchemy.sql import text
import pandas

matplotlib.use('agg')
sns.set(rc={'figure.figsize':(10,5),})

def generate_product_heatmap(db, from_date, product_id):


    # year difference, used for the amount of numbers per row
    from_year = int(from_date.split("-")[0])
    year_diff = 2024 - from_year
    print("Year difference:", year_diff)

    # get all the output transactions within a time frame for a given product
    a = text("""
        SELECT tr.time_registered, tr.product_quantity
        FROM transaction_history tr
        WHERE tr.product_id = :product_id
        AND tr.operation_type_id = 2
        AND tr.time_registered >= :from_date;
    """)

    rs = db.session.execute(a, {'product_id': product_id, 'from_date': from_date})

    months = {
        "Enero": [0 for _ in range(year_diff+1)],
        "Febrero": [0 for _ in range(year_diff+1)],
        "Marzo": [0 for _ in range(year_diff+1)],
        "Abril": [0 for _ in range(year_diff+1)],
        "Mayo": [0 for _ in range(year_diff+1)],
        "Junio": [0 for _ in range(year_diff+1)],
        "Julio": [0 for _ in range(year_diff+1)],
        "Agosto": [0 for _ in range(year_diff+1)],
        "Septiembre": [0 for _ in range(year_diff+1)],
        "Octubre": [0 for _ in range(year_diff+1)],
        "Noviembre": [0 for _ in range(year_diff+1)],
        "Diciembre": [0 for _ in range(year_diff+1)]
    }

    for row in rs:
        month_number = row[0].month
        index_to_change = (row[0].year - from_year)

        if month_number == 1:
            months["Enero"][index_to_change] += row[1]
        elif month_number == 2:
            months["Febrero"][index_to_change] += row[1]
        elif month_number == 3:
            months["Marzo"][index_to_change] += row[1]
        elif month_number == 4:
            months["Abril"][index_to_change] += row[1]
        elif month_number == 5:
            months["Mayo"][index_to_change] += row[1]
        elif month_number == 6:
            months["Junio"][index_to_change] += row[1]
        elif month_number == 7:
            months["Julio"][index_to_change] += row[1]
        elif month_number == 8:
            months["Agosto"][index_to_change] += row[1]
        elif month_number == 9:
            months["Septiembre"][index_to_change] += row[1]
        elif month_number == 10:
            months["Octubre"][index_to_change] += row[1]
        elif month_number == 11:
            months["Noviembre"][index_to_change] += row[1]
        elif month_number == 12:
            months["Diciembre"][index_to_change] += row[1]

    # create a dataframe from the dictionary
    df = pandas.DataFrame(months, index=[str(i) for i in range(from_year, 2024+1)])

    # create the heatmap
    sns.set(rc={'figure.figsize':(18,10),})
    g = sns.heatmap(df, cmap="Reds", annot=True, fmt="d")

    g.set_title("Cantidad de productos vendidos por mes y año", fontsize=30)
    g.set_xlabel("Mes", fontsize=20)
    g.set_ylabel("Año", fontsize=20)

    buf = BytesIO()
    g.figure.savefig(buf, format="png")

    data = base64.b64encode(buf.getbuffer()).decode("utf-8")
    buf.flush()
    buf.close()

    g.figure.clear()

    return data

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

    sns.set_theme(palette="flare")
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
    # set_title
    ax.set_title("Distribución de inventario")

    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
        ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(20)

    buf = BytesIO()
    fig.savefig(buf, format="png")

    data = base64.b64encode(buf.getbuffer()).decode("utf-8")

    buf.flush()
    buf.close()

    fig.clear()

    return data

