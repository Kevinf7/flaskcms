from app import db
from datetime import datetime


# ADMIN STORE models

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    display = db.Column(db.String(40), nullable=True)
    create_date = db.Column(db.DateTime,default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return '<Category {}>'.format(self.name)


class Size(db.Model):
    __tablename__ = 'size'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Size {}>'.format(self.name)


class Color(db.Model):
    __tablename__ = 'color'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Color {}>'.format(self.name)


class CatGenSizeColor(db.Model):
    __tablename__ = 'cat_gen_size_color'
    catgen_id = db.Column(db.Integer, db.ForeignKey('category_general.id'), primary_key=True)
    size_id = db.Column(db.Integer, db.ForeignKey('size.id'), primary_key=True)
    color_id = db.Column(db.Integer, db.ForeignKey('color.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<CatGenSizeColor cat_id: {catgen_id}, size_id: {size_id}, \
            color_id: {color_id}>'.format(catgen_id=self.catgen_id, \
            size_id=self.size_id, color_id=self.color_id)  


class CategoryGeneral(db.Model):
    __tablename__ = 'category_general'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    image_id1 = db.Column(db.Integer, db.ForeignKey('images.id'), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #joined means all rows returned
    #dynamic means return query objects instead of items so you can use filter
    #cascade delete-orphan means if student object is deleted then association table row is also deleted
    size_color = db.relationship('CatGenSizeColor', \
                                    foreign_keys=[CatGenSizeColor.size_id, CatGenSizeColor.color_id], \
                                    backref=db.backref('category_general',lazy='joined'),
                                    lazy='joined',
                                    cascade='all, delete-orphan')
    update_date = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    create_date = db.Column(db.DateTime,default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return '<CategoryGeneral {}>'.format(self.title)






