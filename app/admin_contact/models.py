from app import db
from datetime import datetime


class Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(400), nullable=False)
    user_read = db.Column(db.Boolean, default=False)
    create_date = db.Column(db.DateTime,default=datetime.utcnow, nullable=False)
