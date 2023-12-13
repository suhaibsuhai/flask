from app import admin as db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    fname = db.Column(db.Text)
    lname = db.Column(db.Text)
    email = db.Column(db.Text, unique=True, nullable=False)

