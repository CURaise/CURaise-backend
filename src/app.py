from flask import Flask, request
import json

from db import db

app = Flask(__name__)


db_filename = "database.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/api/', methods=['POST'])
def venmo_test():
    pass



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)