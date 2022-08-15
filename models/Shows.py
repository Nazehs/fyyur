from . import db
from flask_sqlalchemy import inspect


class Shows(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey(
        'venue.id', ondelete='CASCADE'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'artist.id', ondelete='CASCADE'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    artist = db.relationship('Artist', back_populates='upcoming_shows')
    # venue = db.relationship('Venue')

    def toJSON(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
    # venue = db.relationship('Venue')
    # artist = db.relationship('Artist')
