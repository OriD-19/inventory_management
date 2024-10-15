from inventory_app.app import db

class Category(db.Model):
    """
    Original sql code:
    "category_id"	INTEGER NOT NULL,
    "category_name"	TEXT NOT NULL,
    PRIMARY KEY("category_id" AUTOINCREMENT)
    """

    __tablename__ = 'category'

    # sql alchemy ORM translation
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)