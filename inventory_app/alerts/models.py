from inventory_app.app import db

class Alert(db.Model):
    """
    original sql code
    CREATE TABLE "alert" (
        "alert_id"	INTEGER NOT NULL,
        "product_id"	INTEGER NOT NULL,
        "user_id"	INTEGER NOT NULL,
        PRIMARY KEY("alert_id" AUTOINCREMENT),
        FOREIGN KEY("product_id") REFERENCES "product"("product_id"),
        FOREIGN KEY("user_id") REFERENCES "user"("username")
    );
    """

    __tablename__ = 'alert'

    alert_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    product = db.relationship('Product', back_populates='alerts')
    user = db.relationship('User', back_populates='alerts')

    def __repr__(self):
        return f"Alert {self.alert_id} for product {self.product_id} by user {self.user_id}"

