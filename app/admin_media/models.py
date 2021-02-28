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
    create_date = db.Column(db.DateTime,default=datetime.utcnow, nullable=False)

    def getImage(image_id):
        return Images.query.filter_by(id=image_id).first()

    def __repr__(self):
        return '<Images {}>'.format(self.filename)
