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
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    description = db.Column(db.Text)
    img = db.Column(db.String(100))
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))

    category = db.relationship('Category', uselist=False, back_populates='products', lazy=True)
    # get all the transactions associated with a product
    transactions = db.relationship('Transaction', back_populates='product', lazy=True)
    # get all alerts for this product
    alerts = db.relationship('Alert', back_populates='product', lazy=True)

    def __repr__(self):
        return f'<Product {self.product_name}>'
