from flask import current_app
from app import db
from datetime import datetime


# ADMIN PAGE models

class Page(db.Model):
    __tablename__ = 'page'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    page_home = db.relationship(
        "PageHome", backref="page", lazy="dynamic")
    page_contact = db.relationship(
        "PageContact", backref="page", lazy="dynamic")
    update_by = db.Column(db.String(30), nullable=False)
    update_date = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    create_date = db.Column(db.DateTime,default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return '<Page {}>'.format(self.name)


# Add your custom page details below
# The two below are just examples
# The current tables will point to the entry that is currently published
# You also need to create an entry in Page which is like the parent and will be used by Dashboard

class PageHome(db.Model):
    __tablename__ = 'page_home'
    id = db.Column(db.Integer, primary_key=True)
    hero = db.Column(db.String(100))
    section1 = db.Column(db.String(1000))
    section2 = db.Column(db.String(1000))
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=False)
    page_home_curr = db.relationship(
        "PageHomeCurr", backref="page_home", lazy="dynamic")
    update_by = db.Column(db.String(30), nullable=False)
    update_date = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    create_date = db.Column(db.DateTime,default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return '<PageHome {}'.format(self.id)


class PageHomeCurr(db.Model):
    __tablename__ = 'page_home_curr'
    id = db.Column(db.Integer, primary_key=True)
    page_home_id = db.Column(db.Integer, db.ForeignKey('page_home.id'), nullable=False)


class PageContact(db.Model):
    __tablename__ = 'page_contact'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000))
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=False)
    page_contact_curr = db.relationship(
        "PageContactCurr", backref="page_contact", lazy="dynamic")
    update_by = db.Column(db.String(30), nullable=False)
    update_date = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    create_date = db.Column(db.DateTime,default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return '<PageContact {}'.format(self.id)


class PageContactCurr(db.Model):
    __tablename__ = 'page_contact_curr'
    id = db.Column(db.Integer, primary_key=True)
    page_contact_id = db.Column(db.Integer, db.ForeignKey('page_contact.id'), nullable=False)

