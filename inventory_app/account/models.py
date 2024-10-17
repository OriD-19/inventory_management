from inventory_app.app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    """
    Original SQL code:
    CREATE TABLE "user" (
        "username"	TEXT NOT NULL UNIQUE,
        "email"	TEXT NOT NULL UNIQUE,
        "password"	TEXT NOT NULL,
        "created_at"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        "user_role_id"	INTEGER NOT NULL,
        PRIMARY KEY("username"),
        FOREIGN KEY("user_role_id") REFERENCES "user_role"("user_role_id")
    );
    """

    __tablename__ = "user";

    # sqlalchemy orm mapping
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_role_id = db.Column(db.Integer, db.ForeignKey("user_role.user_role_id"), nullable=False)

    # types of user: admin, authorized
    user_role = db.relationship("User_Role", uselist=False, back_populates="users", lazy=True)
    alerts = db.relationship("Alert", back_populates="user", lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.created_at}')"

    def get_id(self):
        return self.user_id

class User_Role(db.Model):
    """
    Original SQL code:
    CREATE TABLE "user_role" (
        "user_role_id"	INTEGER NOT NULL,
        "user_role"	TEXT NOT NULL,
        PRIMARY KEY("user_role_id" AUTOINCREMENT)
    );
    """

    __tablename__ = "user_role";

    # sqlalchemy orm mapping
    user_role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_role = db.Column(db.String(50), unique=True, nullable=False)

    users = db.relationship("User", back_populates="user_role", lazy=True)
