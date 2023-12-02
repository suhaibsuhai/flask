from app import db

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.Text)
    qty = db.Column(db.Integer)
    price = db.Column(db.Float)
    subTotal = db.Column(db.Float)

class Purchases(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Text)
    image = db.Column(db.Text)
    quantity = db.Column(db.Integer)
    date = db.Column(db.Date)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    fname = db.Column(db.Text)
    lname = db.Column(db.Text)
    email = db.Column(db.Text, unique=True, nullable=False)

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.Text)
    price = db.Column(db.Float)
    onSale = db.Column(db.Float)
    onSalePrice = db.Column(db.Float)
    kind = db.Column(db.Text)
