from app import db
from datetime import datetime


# ADMIN MEDIA models

class Images(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50), nullable=False)
    thumbnail = db.Column(db.String(50), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    file_width = db.Column(db.Integer, nullable=False)
    file_height = db.Column(db.Integer, nullable=False)
    image_type_id = db.Column(db.Integer, db.ForeignKey('image_type.id'), nullable=False)
    post = db.relationship('Post', backref='image1', lazy='dynamic')
    page_home_main = db.relationship('PageHomeMain', backref='image1', lazy='dynamic')
    page_home_hero1 = db.relationship('PageHomeHero',
        foreign_keys='PageHomeHero.image_id1', backref='image1', lazy='dynamic')
    page_home_hero2 = db.relationship('PageHomeHero',
        foreign_keys='PageHomeHero.image_id2', backref='image2', lazy='dynamic')
    page_contact = db.relationship('PageContact',
        foreign_keys='PageContact.image_id1', backref='image1', lazy='dynamic')
    page_home_splash = db.relationship('PageHomeSplash',
        foreign_keys='PageHomeSplash.image_id1', backref='image1', lazy='dynamic')
    create_date = db.Column(db.DateTime,default=datetime.utcnow, nullable=False)

    def getImage(image_id):
        return Images.query.filter_by(id=image_id).first()

    def __repr__(self):
        return '<Images {}>'.format(self.filename)


class ImageType(db.Model):
    __tablename__ = 'image_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    images = db.relationship('Images', backref='image_type', lazy='dynamic')

    def __repr__(self):
        return '<ImageType {}>'.format(self.name)
