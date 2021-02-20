from flask import current_app
from app import db


# ADMIN PAGE models

class Page(db.Model, UserMixin):
    __tablename__ = 'page'
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<User {}>'.format(self.id)
