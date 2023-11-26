from src import db
from .club import student_club_association_table


class Student(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    netid = db.Column(db.String, nullable=False, unique=True)
    venmo_username = db.Column(db.String, nullable=False, unique=True)
    clubs = db.relationship("Club", secondary=student_club_association_table, back_populates='members')

    def serialize(self, exclude_venmo_username=False, simplified=False):
        """
        A serialized the output for the student entry.
        :param exclude_venmo_username: whether to exclude the venmo_username.
        :param simplified: whether the output should be simplified.
        :return: a serialized result in a dict.
        """
        venmo_username = {}
        extra = {}

        if not exclude_venmo_username:
            venmo_username = {
                'venmo_username': self.venmo_username,
            }

        if not simplified:
            extra = {
                'clubs': [club.serialize(simplified=simplified) for club in self.clubs]
            }

        return {
            'id': self.id,
            'name': self.name,
            'netid': self.netid,
            **venmo_username,
            **extra
        }
