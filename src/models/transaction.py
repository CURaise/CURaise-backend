from src import db


class Transaction(db.Model):
    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)
    reference_string = db.Column(db.String, nullable=False, unique=True)
    fundraiser = db.Column(db.Integer, db.ForeignKey('fundraiser.id'))

    timestamp = db.Column(db.DateTime, nullable=False)
    item = db.Column(db.Integer, db.ForeignKey('fundraiser_item.id'))
    payer = db.Column(db.Integer, db.ForeignKey('student.id'))

    status = db.Column(db.Boolean, default=False, nullable=False)

    referrer = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=True)

    def serialize(self, simplified=False):
        extra = {}

        if not simplified:
            extra = {
                'referrer': self.referrer
            }

        return {
            'id': self.id,
            'reference_string': self.reference_string,
            'fundraiser': self.fundraiser,
            'timestamp': self.timestamp,
            'item': self.item,
            'payer': self.payer,
            'status': self.status,
            'referrer': self.referrer,
            **extra
        }
