from flask_login import UserMixin

from src import db
from .fundraiser import Fundraiser

# association table to connect Club with Student that is a member
student_club_association_table = db.Table("student_club_association_table", db.Model.metadata,
                                          db.Column("club_id", db.Integer, db.ForeignKey("club.id")),
                                          db.Column("student_id", db.Integer, db.ForeignKey("student.id")),
                                          )


class Club(db.Model, UserMixin):
    __tablename__ = 'club'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    venmo_username = db.Column(db.String, nullable=False)

    members = db.relationship("Student", secondary=student_club_association_table, back_populates='clubs')

    fundraisers = db.relationship('Fundraiser', cascade='delete')

    authenticated = db.Column(db.Boolean, nullable=False, default=False)

    @property
    def is_authenticated(self):
        """
        If the user is authenticated.
        :return: True if authenticated. False otherwise.
        """
        return self.authenticated

    @property
    def is_anonymous(self):
        """
        Return whether the student cna be anonymous
        :return: False, because anonymity is not supported
        """
        return False

    def serialize(self, exclude_venmo_username=False, simplified=False):
        """
        A serialized the output for the club entry.
        :param exclude_venmo_username: whether to exclude the venmo_username.
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
            'fundraisers': [fundraiser.serialize(simplified=True) for fundraiser in self.fundraisers],
            **extra
        }
