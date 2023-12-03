from flask_login import UserMixin

from src import db
from .club import student_club_association_table
from .transaction import Transaction


class Student(db.Model, UserMixin):
    __tablename__ = 'student'
    role = 'student'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    netid = db.Column(db.String, nullable=False, unique=True)

    venmo_username = db.Column(db.String, nullable=False, unique=True)
    venmo_id = db.Column(db.String, nullable=False, unique=True)

    transactions = db.relationship("Transaction")

    clubs = db.relationship("Club", secondary=student_club_association_table, back_populates='members')

    authenticated = db.Column(db.Boolean, nullable=False, default=False)

    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    def get_id(self):
        """
        Get id function for flask_login. It will help in retrieving the user.
        :return:
        """
        return self.role + "_" + str(self.id)

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

    def serialize(self, exclude_venmo_username=False, simplified=False, ios_style=True):
        """
        A serialized the output for the student entry.
        :param exclude_venmo_username: whether to exclude the venmo_username.
        :param simplified: whether the output should be simplified.
        :param ios_style: just return the ios style's serialization
        :return: a serialized result in a dict.
        """

        if ios_style:
            return {
                'id': self.id,
                'name': self.name,
                'venmoUsername': self.venmo_username,
                'transactions': [transaction.serialize(ios_style=True) for transaction in self.transactions]
            }

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
