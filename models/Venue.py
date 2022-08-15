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
    # updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    artist = db.relationship('Artist', secondary='shows',
                             backref=db.backref('venue', lazy=True))
    venues = db.relationship('Shows', backref='venue', lazy=True)
    past_shows = db.relationship('Shows',  lazy=True)
    upcoming_shows = db.relationship('Shows', lazy=True)

    def __repr__(self) -> str:
        return super().__repr__() + '<Venue {}>'.format(self.name)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
