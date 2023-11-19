from . import db
from . import Fundraiser

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
    # FIXME do we need back populates
    members = db.relationship("Student", secondary=student_club_association_table, back_populates=...)

    fundraisers = db.relationship('Fundraiser', cascade='delete')


