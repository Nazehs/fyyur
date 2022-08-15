from . import db


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=True)
    upcoming_shows = db.relationship(
        'Shows', lazy=True, order_by='Shows.start_time', back_populates='artist')
    past_shows = db.relationship(
        'Shows', lazy=True, order_by='Shows.start_time', back_populates='artist')
