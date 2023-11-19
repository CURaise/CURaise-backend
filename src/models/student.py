from . import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    netid = db.Column(db.String, nullable=False, unique=True)
    venmo_username = db.Column(db.String, nullable=False, unique=True)
    clubs = db.Column(db.Integer, db.ForeignKey(''))
