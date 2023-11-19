from . import db

class Fundraiser(db.Model):

    club = db.Column(db.Integer, db.ForeignKey('club.id'))
