from . import db
from flask_sqlalchemy import inspect


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=True)
    venues = db.relationship('Venue', back_populates='artist')

    def __repr__(self):
        return ' {0}'.format(self.name)

    def toJSON(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class Shows(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey(
        'venue.id', ondelete='CASCADE'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'artist.id', ondelete='CASCADE'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

    def toJSON(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_description = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean(), default=False)
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    artist = db.relationship(
        'Artist',  back_populates='venues')

    def __repr__(self):
        return '{0}'.format(self.name)

    def toJSON(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
