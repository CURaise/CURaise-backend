from src import db

fundraiser_item_transaction_association_table = db.Table(
    'fundraiser_item_transaction_association_table', db.Model.metadata,
    db.Column('FundraiserItem_id', db.Integer, db.ForeignKey('fundraiser_item.id')),
    db.Column('Transaction_id', db.Integer, db.ForeignKey('transaction.id'))
)

class FundraiserItem(db.Model):
    __tablename__ = "fundraiser_item"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String)

    fundraiser = db.Column(db.Integer, db.ForeignKey('fundraiser.id'))
    transactions = db.relationship('Transaction', secondary=fundraiser_item_transaction_association_table,
                                   back_populates='items')

    def serialize(self, simplified=False, ios_style=True):
        """
        A serialized the output for the fundraiser item entry.
        :param simplified: whether the output should be simplified.
        :param ios_style: just return the ios style's serialization
        :return: a serialized result in a dict.
        """
        if ios_style:
            return {
                'id': self.id,
                'name': self.name,
                'price': self.price,
                'description': self.description
            }

        extra = {}
        if not simplified:
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
