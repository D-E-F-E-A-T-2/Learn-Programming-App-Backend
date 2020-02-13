from LPapp import db
from datetime import datetime


class Users(db.Model):

    # pk is email
    """
    API call will interact with Users table
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(100)) #bcrypt storage needs 60 size
    email = db.Column(db.String(60), unique=True)
    admin_status = db.Column(db.Boolean, nullable=False, default=0)