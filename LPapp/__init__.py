import os

# externals
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS


app = Flask(__name__)
CORS(app, support_credentials=True)
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('STRIPE_API_KEY')

basedir = os.path.abspath(os.path.dirname(__file__))

PG = os.environ.get("DATABASE_URL")

if PG is None or PG=="":
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
        os.path.join(basedir, 'db.sqlite')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = PG
    
db = SQLAlchemy(app)

from LPapp import routes
