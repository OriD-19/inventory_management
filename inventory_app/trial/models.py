from inventory_app.app import db

class Trial(db.Model):
    __tablename__ = 'category'

    category_id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Trial {self.name}>'