from datetime import datetime

from src import db
from src.utils import DATETIME_FORMAT
from src.models.fundraiser_item import fundraiser_item_transaction_association_table
from src.models import Fundraiser


class Transaction(db.Model):
    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)
    reference_string = db.Column(db.String, nullable=False, unique=True)
    fundraiser = db.Column(db.Integer, db.ForeignKey('fundraiser.id'))

    added_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    items = db.relationship('FundraiserItem', secondary=fundraiser_item_transaction_association_table,
                            back_populates='transactions')
    club = db.Column(db.Integer, db.ForeignKey('club.id'))
    payer_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    status = db.Column(db.Boolean, default=False, nullable=False)

    # referrer_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=True)

    def serialize(self, simplified=False, ios_style=True):
        """
        A serialized the output for the transaction entry.
        :param simplified: whether the output should be simplified.
        :return: a serialized result in a dict.
        """

        if ios_style:
            return {
                'id': self.id,
                'referenceString': self.reference_string,
                'fundraiser': Fundraiser.query.get({'id': self.fundraiser}).serialize(ios_style=True),
                'timestamp': str(self.added_timestamp.strftime(DATETIME_FORMAT)),
                'items': [item.serialize(ios_style=True) for item in self.items],
                'buyerId': self.payer_id,
                'transactionComplete': self.status
            }

        extra = {}

        if not simplified:
            extra = {
                'referrer': self.referrer
            }

        return {
            'id': self.id,
            'reference_string': self.reference_string,
            'fundraiser': self.fundraiser.serialize(ios_style=True),
            'timestamp': self.added_timestamp,
            'item': self.item,
            'payer': self.payer,
            'status': self.status,
            'referrer': self.referrer,
            **extra
        }
