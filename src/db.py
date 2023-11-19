from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Club(db.Model):
    __tablename__ = 'club'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
