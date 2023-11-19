from src import db

class FundraiserItem(db.Model):
    __tablename__ = "fundraiser_item"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String)

    # fundraiser = db.relationship()
    # transactions = db.