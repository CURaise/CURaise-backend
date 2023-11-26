from src import db
from .fundraiser import Fundraiser

# association table to connect Club with Student that is a member
student_club_association_table = db.Table("student-club association", db.Model.metadata,
    db.Column("club_id", db.Integer, db.ForeignKey("club.id")),
    db.Column("student_id", db.Integer, db.ForeignKey("student.id")),
)


class Club(db.Model):
    __tablename__='club'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    venmo_username = db.Column(db.String, nullable=False)

    members = db.relationship("Student", secondary=student_club_association_table, back_populates='clubs')

    fundraisers = db.relationship('Fundraiser', cascade='delete')

    def serialize(self, simplified=False):
        """
        A serialized the output for the club entry.
        :param simplified: whether the output should be simplified.
        :return: the serialized result in a dict.
        """
        extra = {}

        if not simplified:
            extra = {
                'description': self.description,
                'venmo_username': self.venmo_username,
                'members': [member.serialize(simplified=True) for member in self.members]
            }

        return {
            'id': self.id,
            'name': self.name,
            **extra
        }