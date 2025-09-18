from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    artnr = db.Column(db.String(20), unique=False, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    ean = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<Item {self.name} ({self.quantity})>'

