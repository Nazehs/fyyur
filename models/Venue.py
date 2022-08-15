from . import db


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_description = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean(), default=False)
    genres = db.Column(db.ARRAY(db.String))
    artist = db.relationship(
        'Artist',  backref='venues')
    upcoming_shows = db.relationship(
        'Shows', lazy=True, backref='venue', order_by='Shows.start_time')

    past_shows = db.relationship(
        'Shows', lazy=True,  order_by='Shows.start_time')

    def __repr__(self) -> str:
        return super().__repr__() + '<Venue {}>'.format(self.name)
