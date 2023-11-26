from src import db


class FundraiserItem(db.Model):
    __tablename__ = "fundraiser_item"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String)

    fundraiser = db.Column(db.Integer, db.ForeignKey('fundraiser.id'))
    transactions = db.relationship('Transaction', cascade='delete')

    def serialize(self, simplified=False):
        """
        A serialized the output for the fundraiser item entry.
        :param simplified: whether the output should be simplified.
        :return: a serialized result in a dict.
        """
        extra = {}
        if not extra:
            extra = {
                'transactions': [transaction.serialize(simplified=True) for transaction in self.transactions]
            }

        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'fundraiser': self.fundraiser,
            **extra
        }
