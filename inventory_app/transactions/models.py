from inventory_app.app import db

class TransactionHistory(db.Model):
    """
    Original sql code:
    "transaction_id"	INTEGER NOT NULL,
	"product_id"	INTEGER NOT NULL,
	"product_quantity"	INTEGER NOT NULL,
	"time_registered"	TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"operation_type_id"	INTEGER,
	PRIMARY KEY("transaction_id" AUTOINCREMENT),
	FOREIGN KEY("operation_type_id") REFERENCES "operation_type"("operation_type_id"),
	FOREIGN KEY("product_id") REFERENCES "product"("product_id")
    """

    __tablename__ = 'transaction_history'

    # sql alchemy ORM translation
    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_quantity = db.Column(db.Integer, nullable=False)
    time_registered = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())

    operation_type_id = db.Column(db.Integer, db.ForeignKey('operation_type.operation_type_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)

    product = db.relationship('Product', uselist=False, back_populates='transactions', lazy=True)
    operation = db.relationship('OperationType', uselist=False, back_populates='transactions', lazy=True)

class OperationType(db.Model):
    """
    Original sql code:
    "operation_type_id"	INTEGER NOT NULL,
    "operation_name"	TEXT NOT NULL,
    PRIMARY KEY("operation_type_id" AUTOINCREMENT)
    """

    __tablename__ = 'operation_type'

    # sql alchemy ORM translation
    operation_type_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    operation_name = db.Column(db.String(100), nullable=False)

    # get all the transactions from a certain type (in/out)
    transactions = db.relationship('TransactionHistory', back_populates='operation', lazy=True)
