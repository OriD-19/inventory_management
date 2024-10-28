from inventory_app.app import db

class Alert(db.Model):

    __tablename__ = 'alert'

    alert_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_alert_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    user_alert_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    min_product_stock = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', back_populates='alerts')
    product = db.relationship('Product', back_populates='alerts')
