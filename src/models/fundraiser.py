from src import db
from datetime import datetime
from src.utils import DATETIME_FORMAT


class Fundraiser(db.Model):
    __tablename__ = 'fundraiser'


    id = db.Column(db.Integer, primary_key=True)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'))
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    active_status = db.Column(db.Boolean, default=False, nullable=False)

    created_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    last_modified_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)

    items = db.relationship('FundraiserItem', cascade='delete')

    def serialize(self, simplified=False):
        """
        A serialized the output for the fundraiser event entry.
        :param simplified: whether the output should be simplified.
        :return: a serialized result in a dict.
        """
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

            'created_datetime': str(self.created_datetime.strftime(DATETIME_FORMAT)),
            'last_modified_datetime': str(self.last_modified_datetime.strftime(DATETIME_FORMAT)),
            'start_datetime': str(self.start_datetime.strftime(DATETIME_FORMAT)),
            'end_datetime': str(self.end_datetime.strftime(DATETIME_FORMAT)),

            **extra,
        }
