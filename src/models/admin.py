from flask_login import UserMixin

from src import db
from .club import student_club_association_table


class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'
    role = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    authenticated = db.Column(db.Boolean, nullable=False, default=False)

    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    def get_id(self):
        """
        Get id function for flask_login. It will help in retrieving the user.
        :return:
        """
        return self.role + "_" + str(id)

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
        Return whether the user cna be anonymous
        :return: False, because anonymity is not supported
        """
        return False

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }
