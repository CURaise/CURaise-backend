import json

from src import db
from .fundraiser import Fundraiser

# association table to connect Club with Student that is a member
student_club_association_table = db.Table("student_club_association_table", db.Model.metadata,
                                          db.Column("club_id", db.Integer, db.ForeignKey("club.id")),
                                          db.Column("student_id", db.Integer, db.ForeignKey("student.id")),
                                          )


class Club(db.Model):
    __tablename__ = 'club'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    venmo_username = db.Column(db.String, nullable=False)

    members = db.relationship("Student", secondary=student_club_association_table, back_populates='clubs')

    fundraisers = db.relationship('Fundraiser', cascade='delete')

    def serialize(self, exclude_venmo_username=False, simplified=False):
        """
        A serialized the output for the club entry.
        :param exclude_venmo_username: whether to include the venmo_username.
        :param simplified: whether the output should be simplified.
        :return: a serialized result in a dict.
        """
        venmo_username = {}
        extra = {}

        if not exclude_venmo_username:
            venmo_username = {
                'venmo_username': self.venmo_username
            }

        if not simplified:
            extra = {
                'members': [member.serialize(simplified=True) for member in self.members]
            }

        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            **venmo_username,
            **extra
        }
