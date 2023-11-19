from . import db


class Student(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    netid = db.Column(db.String, nullable=False, unique=True)
    venmo_username = db.Column(db.String, nullable=False, unique=True)
    clubs = db.Column(db.Integer, db.ForeignKey(''))
