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
    # upcoming_shows = db.relationship(
    #     'Venue', secondary='shows', backref='venues', lazy=True)
    upcoming_shows = db.relationship('Shows', lazy=True)
    # genres = db.relationship('Genre', secondary=table,
    #                          backref=db.backref('artists', lazy=True))

    # updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
