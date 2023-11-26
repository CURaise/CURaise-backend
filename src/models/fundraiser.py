from src import db


class Fundraiser(db.Model):
    __tablename__ = 'fundraiser'

    id = db.Column(db.Integer, primary_key=True)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'))
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    active_status = db.Column(db.Boolean, default=False, nullable=False)
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)

    items = db.relationship('FundraiserItem', cascade='delete')

    def serialize(self, simplified=False):
        extra = {}
        if not simplified:
            extra = {
                'items': [item.serialize(simplified=True) for item in self.items]
            }

        return {
            'id': self.id,
            'club_id': self.club_id,
            'title': self.title,
            'description': self.description,
            'active_status': self.active_status,
            'start_datetime': self.start_datetime,
            'end_datetime': self.end_datetime,
            **extra,
        }
