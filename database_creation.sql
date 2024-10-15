-- code for reference only

CREATE TABLE "category" (
	"category_id"	INTEGER NOT NULL,
	"category"	TEXT NOT NULL,
	PRIMARY KEY("category_id" AUTOINCREMENT)
);

CREATE TABLE "product" (
	"product_id"	INTEGER NOT NULL,
	"product_name"	TEXT NOT NULL,
	"stock"	INTEGER NOT NULL DEFAULT 0,
	"description"	TEXT,
	"img"	TEXT,
	"category_id"	INTEGER,
	PRIMARY KEY("product_id" AUTOINCREMENT),
	FOREIGN KEY("category_id") REFERENCES "category"("category_id")
);

ALTER TABLE product ADD price REAL NOT NULL DEFAULT 0.01;

CREATE TABLE "user_role" (
	"user_role_id"	INTEGER NOT NULL,
	"user_role"	TEXT NOT NULL,
	PRIMARY KEY("user_role_id" AUTOINCREMENT)
);

CREATE TABLE "operation_type" (
	"operation_type_id"	INTEGER NOT NULL,
	"operation_type"	TEXT NOT NULL,
	PRIMARY KEY("operation_type_id" AUTOINCREMENT)
);

CREATE TABLE "transaction_history" (
	"transaction_id"	INTEGER NOT NULL,
	"product_id"	INTEGER NOT NULL,
	"product_quantity"	INTEGER NOT NULL,
	"time_registered"	TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"operation_type_id"	INTEGER,
	PRIMARY KEY("transaction_id" AUTOINCREMENT),
	FOREIGN KEY("operation_type_id") REFERENCES "operation_type"("operation_type_id"),
	FOREIGN KEY("product_id") REFERENCES "product"("product_id")
);

CREATE TABLE "user" (
	"username"	TEXT NOT NULL UNIQUE,
	"email"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	"created_at"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	"user_role_id"	INTEGER NOT NULL,
	PRIMARY KEY("username"),
	FOREIGN KEY("user_role_id") REFERENCES "user_role"("user_role_id")
);

CREATE TABLE "alert" (
	"alert_id"	INTEGER NOT NULL,
	"product_id"	INTEGER NOT NULL,
	"user_id"	INTEGER NOT NULL,
	PRIMARY KEY("alert_id" AUTOINCREMENT),
	FOREIGN KEY("product_id") REFERENCES "product"("product_id"),
	FOREIGN KEY("user_id") REFERENCES "user"("username")
);

CREATE TRIGGER register_transaction AFTER INSERT ON transaction_history
BEGIN
  UPDATE product
  SET stock =
  CASE WHEN NEW.operation_type_id == 1 --entrance of products
    THEN stock + NEW.product_quantity
    ELSE stock - NEW.product_quantity
  END
  WHERE product_id = NEW.product_id;
END

