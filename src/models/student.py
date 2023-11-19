from src import db
from .club import student_club_association_table


class Student(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    netid = db.Column(db.String, nullable=False, unique=True)
    venmo_username = db.Column(db.String, nullable=False, unique=True)
    clubs = db.Column(db.Integer, db.ForeignKey(''))

    def serialize(self, simplified=False):
        """
        A serialized the output for the student entry.
        :param simplified: whether the output should be simplified.
        :return: the serialized result in a dict.
        """
        extra = {}
        if not simplified:
            extra = {
                'venmo_username': self.venmo_username,
                'clubs': [club.serialize(simplified=simplified) for club in self.clubs]
            }

        return {
            'id': self.id,
            'name': self.name,
            'netid': self.netid,
            **extra
        }