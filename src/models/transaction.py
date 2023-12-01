from datetime import datetime

from src import db


class Transaction(db.Model):
    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)
    reference_string = db.Column(db.String, nullable=False, unique=True)
    fundraiser = db.Column(db.Integer, db.ForeignKey('fundraiser.id'))

    added_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    item = db.Column(db.Integer, db.ForeignKey('fundraiser_item.id'))
    club = db.Column(db.Integer, db.ForeignKey('club.id'))
    payer = db.Column(db.Integer, db.ForeignKey('student.id'))

    status = db.Column(db.Boolean, default=False, nullable=False)

    referrer = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=True)

    def serialize(self, simplified=False):
        """
        A serialized the output for the transaction entry.
        :param simplified: whether the output should be simplified.
        :return: a serialized result in a dict.
        """

        extra = {}

        if not simplified:
            extra = {
                'referrer': self.referrer
            }

        return {
            'id': self.id,
            'reference_string': self.reference_string,
            'fundraiser': self.fundraiser,
            'timestamp': self.added_timestamp,
            'item': self.item,
            'payer': self.payer,
            'status': self.status,
            'referrer': self.referrer,
            **extra
        }
