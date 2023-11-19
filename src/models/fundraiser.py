from src import db


class Fundraiser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    club = db.Column(db.Integer, db.ForeignKey('club.id'))