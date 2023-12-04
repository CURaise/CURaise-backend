from flask_sqlalchemy import SQLAlchemy
from venmo_api import Client
from flask_login import LoginManager

import dotenv
# import pyrebase

import os

import firebase_admin
from firebase_admin import credentials, auth

dotenv.load_dotenv()

db = SQLAlchemy()
client = Client(access_token=os.environ["VENMO_TOKEN"], )
login_manager = LoginManager()

cred = credentials.Certificate("firebase_creds.json")
firebase_admin.initialize_app(cred)

# firebase_config = {
#   "apiKey": os.environ['FIREBASE_APIKEY'],
#   "authDomain": "curaise.firebaseapp.com",
#   "projectId": "curaise",
#   "storageBucket": "curaise.appspot.com",
#   "messagingSenderId": "858565940703",
#   "appId": "1:858565940703:web:ab8cc43b615b7f5b07a06a",
#   "measurementId": "G-CDWT3HPQ7T"
# }
#
# firebase = pyrebase.initialize_app(firebase_config)
# auth = firebase.auth()
