from inventory_app.app import db

class Product(db.Model):
    """
    Original sql code:
	"product_id"	INTEGER NOT NULL,
	"product_name"	TEXT NOT NULL,
	"stock"	INTEGER NOT NULL DEFAULT 0,
	"description"	TEXT,
	"img"	TEXT,
	"category_id"	INTEGER,
	PRIMARY KEY("product_id" AUTOINCREMENT),
	FOREIGN KEY("category_id") REFERENCES "category"("category_id")
    """

    __tablename__ = 'product'

    # sql alchemy ORM translation
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    description = db.Column(db.Text)
    img = db.Column(db.String(100))
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))