#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import os
import dateutil.parser
import babel
from flask import render_template, request, flash, redirect, url_for
from flask_moment import Moment
from sqlalchemy.exc import SQLAlchemyError
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from forms import *
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

# models and database
from models import app, db
from models.Artist import Artist
from models.Shows import Shows
from models.Venue import Venue
moment = Moment(app)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/band_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


# table = db.Table('genre_artist', db.Column('artist_id', db.Integer, db.ForeignKey(
#     'artist.id')), db.Column('genre_id', db.Integer, db.ForeignKey('genre.id')))

# # table2 = db.Table('genre', db.Column('artist_id', db.Integer, db.ForeignKey('artist.id')), db.Column('venue_id', db.Integer, db.ForeignKey('venue.id')))


# class Genre(db.Model):
#     __tablename__ = 'genre'
#     name = db.Column(db.String, nullable=False)
#     id = db.Column(db.Integer, primary_key=True)

#     def __repr__(self) -> str:
#         return f'{0}'.format(self.name)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@ app.route('/', methods=['GET', 'POST'])
def index():

    recent_venues = Venue.query.order_by(Venue.id.desc()).limit(5).all()
    recent_artists = Artist.query.order_by(Artist.id.desc()).limit(5).all()
    return render_template('pages/home.html', recent_venues=recent_venues, recent_artists=recent_artists)


#  Venues
#  ----------------------------------------------------------------

@ app.route('/venues')
def venues():
    #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.

    venues = Venue.query.order_by('id').all()
    dataObj = []
    for v in venues:
        isCityAdded = list(
            filter(lambda d: d[1]['city'] == v.city, enumerate(dataObj)))
        if len(isCityAdded) == 0:
            obj = {
                "city": v.city,
                "state": v.state,
                "venues": [{
                    "id": v.id,
                    "name": v.name,
                    "num_upcoming_shows": 0,
                }]
            }
            dataObj.append(obj)
        else:
            print(isCityAdded[0][0])
            dataObj[isCityAdded[0][0]]['venues'].append({
                "id": v.id,
                "name": v.name,
                "num_upcoming_shows": 0,

            })

    return render_template('pages/venues.html', areas=dataObj)


@ app.route('/venues/search', methods=['POST'])
def search_venues():

    searchTerm = request.form['search_term']
    query = Venue.query.filter(Venue.name.ilike(
        '%' + request.form['search_term'] + '%')).all()
    response = {
        "count": len(query),
        "data": query}
    return render_template('pages/search_venues.html', results=response, search_term=searchTerm)


@ app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    data = Venue.query.get(venue_id)
    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@ app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@ app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    try:
        form = VenueForm(request.form)
        venueData = Venue(name=form.name.data,
                          city=form.city.data,
                          state=form.state.data,
                          phone=form.phone.data,
                          image_link=form.image_link.data,
                          facebook_link=form.facebook_link.data,
                          seeking_talent=form.seeking_talent.data,
                          website_link=form.website_link.data,
                          genres=form.genres.data,
                          seeking_description=form.seeking_description.data)
        db.session.add(venueData)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        db.session.rollback()
        flash('An error occurred. Venue' +
              request.form['name'] + ' could not be listed.')
    finally:
        db.session.close()
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
        flash('Venue was successfully deleted')
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        flash('An error occurred. could not delete venue.')
    finally:
        db.session.close()
    return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------


@ app.route('/artists')
def artists():
    print(Artist.query.all())
    print(Artist.query.order_by('id').all())
    return render_template('pages/artists.html', artists=Artist.query.order_by('id').all())


@ app.route('/artists/search', methods=['POST'])
def search_artists():
    query = Artist.query.filter(Artist.name.ilike(
        '%' + request.form['search_term'] + '%')).all()
    response = {
        'count': len(query),
        'data': query
    }

    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@ app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id
    data = Artist.query.get(artist_id)
    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------


@ app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    form.genres.data = artist.genres
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@ app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    try:

        form = ArtistForm(obj=request.form)
        data = dict(form.data)
        del data['csrf_token']
        Artist.query.filter_by(id=artist_id).update(data)
        db.session.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@ app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.filter_by(id=venue_id).first()
    form.genres.data = venue.genres

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@ app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    try:
        form = VenueForm(obj=request.form)
        data = dict(form.data)
        del data['csrf_token']
        Venue.query.filter_by(id=venue_id).update(data)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@ app.route('/artists/create', methods=['GET'])
def create_artist_form():
    # try:
    form = ArtistForm()
    #     artist = Artist.create(form)
    #     db.session.add(artist)
    #     db.session.commit()
    # except:
    #     db.session.rollback()
    # finally:
    #     db.session.close()
    return render_template('forms/new_artist.html', form=form)


@ app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    error = False
    try:
        form = ArtistForm(request.form)
        artist = Artist(
            name=form.name.data,
            city=form.city.data,
            state=form.state.data,
            phone=form.phone.data,
            genres=form.genres.data,
            image_link=form.image_link.data,
            facebook_link=form.facebook_link.data,
            seeking_venue=form.seeking_venue.data,
            website_link=form.website_link.data,
            seeking_description=form.seeking_description.data
        )
        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        db.session.rollback()
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be listed.')
    finally:
        db.session.close()
    return redirect(url_for('index'))


@app.route('/artist/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    try:
        Artist.query.filter_by(id=artist_id).delete()
        db.session.commit()
        flash('Artist was successfully deleted')
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        db.session.rollback()
        flash('Oops! An error occurred. Artist could not be deleted.')
    finally:
        db.session.close()
    return redirect(url_for('index'))

#  Shows
#  ----------------------------------------------------------------


@ app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    data = [{
        "venue_id": 1,
        "venue_name": "The Musical Hop",
        "artist_id": 4,
        "artist_name": "Guns N Petals",
        "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        "start_time": "2019-05-21T21:30:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 5,
        "artist_name": "Matt Quevedo",
        "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        "start_time": "2019-06-15T23:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-01T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-08T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-15T20:00:00.000Z"
    }]


# Shows.query.order_by('id').all()
    query = Shows.query.order_by('id').all()
    for show in query:
        print(show.toJSON())
        print(show.artist_id)
        print(show.venue_id)
        print(show.start_time)
    return render_template('pages/shows.html', shows=query)


@ app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@ app.route('/shows/create', methods=['POST'])
def create_show_submission():
    error = False
    try:
        show = Shows(
            artist_id=request.form['artist_id'],
            venue_id=request.form['venue_id'],
            start_time=request.form['start_time']
        )
        db.session.add(show)
        db.session.commit()
        flash('Show was successfully listed!')
    except:
        error = True
        db.session.rollback()
        flash('An error occurred. Show could not be listed.')
        print(sys.exc_info())
    finally:
        db.session.close()
    return redirect(url_for('index'))


@ app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@ app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
# if __name__ == '__main__':
#     app.run()

# Or specify port manually:

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port)
