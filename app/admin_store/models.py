from app import db
from datetime import datetime


# ADMIN STORE models

class Catalog(db.Model):
    __tablename__ = 'catalog'
    id = db.Column(db.Integer, primary_key=True)
    create_date = db.Column(db.DateTime,default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return '<Page {}>'.format(self.name)


class CatalogStatus(db.Model):
    __tablename__ = 'catalog_status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    create_date = db.Column(db.DateTime,default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return '<PageStatus {}>'.format(self.name)


# Just an example
class CatalogBook(db.Model):
    __tablename__ = 'catalog_book'
    id = db.Column(db.Integer, primary_key=True)
    image_id1 = db.Column(db.Integer, db.ForeignKey('images.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('page_status.id'), nullable=False)
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    update_date = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    create_date = db.Column(db.DateTime,default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return '<CatalogBook {}>'.format(self.id)



