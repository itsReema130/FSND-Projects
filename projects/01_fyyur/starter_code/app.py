#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import sys

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app , db)
# Done: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

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

    # DONE: implement any missing fields, as a database migration using Flask-Migrate
    genres = db.Column(db.String(120),nullable=True)
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean,default=False)
    seeking_description = db.Column(db.Text)
    upcoming_shows_count = db.Column(db.Integer, default=0)
    past_shows_count = db.Column(db.Integer, default=0)
    shows = db.relationship('Show',backref='venue',lazy=True, cascade="save-update, merge, delete")


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # DONE: implement any missing fields, as a database migration using Flask-Migrate
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean,default=False)
    seeking_description = db.Column(db.Text)
    upcoming_shows_count = db.Column(db.Integer, default=0)
    past_shows_count = db.Column(db.Integer, default=0)
    shows = db.relationship('Show',backref='artist',lazy=True,cascade="save-update, merge, delete")

# DONE Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    start_time = db.Column(db.DateTime)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # DONE: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

    listVanue = Venue.query.group_by(Venue.id, Venue.state, Venue.city).all()
    data = []

    upcomingshows = (
        db.session.query(Show)
        .filter(Show.venue_id == 1)
        .filter(Show.start_time > datetime.now())
        .all()
    )
    for area in listVanue:
        area_venues = (
            Venue.query.filter_by(state=area.state).filter_by(city=area.city).all()
        )
        VenuesData = []
        for venue in area_venues:
            VenuesData.append(
                {
                    "id": venue.id,
                    "name": venue.name,
                    "num_upcoming_shows": len(upcomingshows),
                }
            )
        data.append({"city": area.city, 
        "state": area.state, 
        "venues": VenuesData})

    return render_template('pages/venues.html', areas=data);

    

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    results = Venue.query.filter(Venue.name.ilike('%{}%'.format(request.form['search_term']))).all()
    response={
    "count": len(results),
    "data": []}
    for venue in results:
      response["data"].append({
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": venue.upcoming_shows_count
      })
  
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # DONE: replace with real venue data from the venues table, using venue_id
    ven = db.session.query(Venue).get(venue_id)
    show_query = db.session.query(Show).join(Venue).filter(venue_id == Show.venue_id)
    upcoming_shows = []
    past_shows = []

    for show in show_query: 
        showDate = show.start_time
        if showDate > datetime.now():
            upcoming_shows.append({'venue_id': show.venue_id,'Venue_name': db.session.query(Venue).get(show.venue_id).name,'venue_image_link': db.session.query(Venue).get(show.venue_id).image_link,'start_time': str(show.start_time)})
        else:
            past_shows.append({'venue_id': show.venue_id,'venue_name': db.session.query(Venue).get(show.venue_id).name,'venue_image_link': db.session.query(Venue).get(show.venue_id).image_link,'start_time': str(show.start_time)})

    DataV = {
        'id': ven.id,
        'name': ven.name,
        'genres': ven.genres,
        'address': ven.address,
        'city': ven.city,
        'state': ven.state,
        'phone': ven.phone,
        'facebook_link': ven.facebook_link,
        'website_link': ven.website,
        'seeking_talent': ven.seeking_talent,
        'seeking_description': ven.seeking_description,
        'image_link': ven.image_link,
        'past_shows': past_shows,
        'upcoming_shows': upcoming_shows,
        'past_shows_count': len(past_shows),
        'upcoming_shows_count': len(upcoming_shows)} 
    return render_template('pages/show_venue.html', venue=DataV)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # DONE: insert form data as a new Venue record in the db, instead
  # DONE: modify data to be the data object returned from db insertion
  
  new_venue = Venue()
  new_venue.name = request.form['name']
  new_venue.city = request.form['city']
  new_venue.state = request.form['state']
  new_venue.address = request.form['address']
  new_venue.phone = request.form['phone']
  new_venue.image_link = request.form['image_link']
  new_venue.genres = request.form['genres']
  new_venue.facebook_link = request.form['facebook_link']
  new_venue.website = request.form['website_link']
  new_venue.seeking_talent = True if 'seeking_talent' in request.form else False
  new_venue.seeking_description = request.form['seeking_description']

  try:
  
    db.session.add(new_venue)
    db.session.commit()
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:

    db.session.rollback()
    print(sys.exc_info())
    # DONE: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  finally:
    db.session.close()
  return redirect(url_for('index'))


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # DONE: Complete this endpoint for taking a venue_id, and using
  error = False
  try:
    venueById = Venue.query.get(venue_id)
    db.session.delete(venueById)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error: 
    flash(f'An error occurred. Venue {venue_id} could not be deleted.')
  if not error: 
    flash(f'Venue {venue_id} was successfully deleted.')
  return render_template('pages/home.html')
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # Done: replace with real data returned from querying the database
  
  Artist_data= Artist.query.group_by(Artist.id, Artist.name).all()
  return render_template('pages/artists.html', artists=Artist_data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
    results = Artist.query.filter(Artist.name.ilike('%{}%'.format(request.form['search_term']))).all()
    response={
    "count": len(results),
    "data": []}
    for artist in results:
      response["data"].append({
        "id": artist.id,
        "name": artist.name,
        "num_upcoming_shows": artist.upcoming_shows_count
      })
  
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # DONE: replace with real artist data from the artist table, using artist_id
    art = db.session.query(Artist).get(artist_id)
    show_query = db.session.query(Show).join(Artist).filter(artist_id == Show.artist_id)
    upcoming_shows = []
    past_shows = []

    for show in show_query: 
        showDate = show.start_time
        if showDate > datetime.now():
            upcoming_shows.append({'artist_id': show.artist_id,'artist_name': db.session.query(Artist).get(show.artist_id).name,'artist_image_link': db.session.query(Artist).get(show.artist_id).image_link,'start_time': str(show.start_time)})
        else:
            past_shows.append({'artist_id': show.artist_id,'artist_name': db.session.query(Artist).get(show.artist_id).name,'artist_image_link': db.session.query(Artist).get(show.artist_id).image_link,'start_time': str(show.start_time)})

    DataArt = {
        'id': art.id,
        'name': art.name,
        'city': art.city,
        'state': art.state,
        'phone': art.phone,
        'image_link': art.image_link,
        'genres': art.genres,
        'facebook_link': art.facebook_link,
        'website_link':art.website,
        'seeking_venue': art.seeking_venue,
        'seeking_description': art.seeking_description,
        'past_shows': past_shows,
        'upcoming_shows': upcoming_shows,
        'past_shows_count': len(past_shows),
        'upcoming_shows_count': len(upcoming_shows)} 
    return render_template('pages/show_artist.html', artist=DataArt)


  

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  oldArtistData = Artist.query.get(artist_id)

  if oldArtistData: 
    form.name.data = oldArtistData.name
    form.city.data = oldArtistData.city
    form.state.data = oldArtistData.state
    form.phone.data = oldArtistData.phone
    form.image_link.data = oldArtistData.image_link
    form.genres.data = oldArtistData.genres
    form.facebook_link.data = oldArtistData.facebook_link
    form.website_link.data = oldArtistData.website
    form.seeking_venue.data = oldArtistData.seeking_venue
    form.seeking_description.data = oldArtistData.seeking_description
  # DONE: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=oldArtistData)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # DONE: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  error = False  
  newArtistData = Artist.query.get(artist_id)

  try: 
    newArtistData.name = request.form['name']
    newArtistData.city = request.form['city']
    newArtistData.state = request.form['state']
    newArtistData.phone = request.form['phone']
    newArtistData.genres = request.form['genres']
    newArtistData.image_link = request.form['image_link']
    newArtistData.facebook_link = request.form['facebook_link']
    newArtistData.website= request.form['website_link']
    newArtistData.seeking_venue = True if 'seeking_venue' in request.form else False 
    newArtistData.seeking_description = request.form['seeking_description']

    db.session.commit()
  except: 
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally: 
    db.session.close()
  if error: 
    flash('An error occurred. Artist could not be Updated.')
  if not error: 
    flash('Artist was successfully updated!')
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  form = VenueForm()
  oldVenueData = Venue.query.get(venue_id)

  if oldVenueData: 
    form.name.data = oldVenueData.name
    form.city.data = oldVenueData.city
    form.state.data = oldVenueData.state
    form.address.data = oldVenueData.address
    form.phone.data = oldVenueData.phone
    form.genres.data = oldVenueData.genres
    form.facebook_link.data = oldVenueData.facebook_link
    form.image_link.data = oldVenueData.image_link
    form.website_link.data = oldVenueData.website
    form.seeking_talent.data = oldVenueData.seeking_talent
    form.seeking_description.data = oldVenueData.seeking_description

  # DONE: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=oldVenueData)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # DONE: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  error = False  
  newVenuetData = Venue.query.get(venue_id)

  try: 
    newVenuetData.name = request.form['name']
    newVenuetData.city = request.form['city']
    newVenuetData.state = request.form['state']
    newVenuetData.address =request.form['address']
    newVenuetData.phone = request.form['phone']
    newVenuetData.image_link = request.form['image_link']
    newVenuetData.genres = request.form['genres']
    newVenuetData.facebook_link = request.form['facebook_link']
    newVenuetData.website= request.form['website_link']
    newVenuetData.seeking_venue = True if 'seeking_venue' in request.form else False 
    newVenuetData.seeking_description = request.form['seeking_description']

    db.session.commit()
  except: 
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally: 
    db.session.close()
  if error: 
    flash('An error occurred. Artist could not be Updated.')
  if not error: 
    flash('Artist was successfully updated!')

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # DONE: insert form data as a new Venue record in the db, instead
  # DONE: modify data to be the data object returned from db insertion
  newArtist= Artist()
  newArtist.name= request.form['name']
  newArtist.city=request.form['city']
  newArtist.state=request.form['state']
  newArtist.phone=request.form['phone']
  newArtist.image_link=request.form['image_link']
  newArtist.genres= request.form['genres']
  newArtist.facebook_link=request.form['facebook_link']
  newArtist.website_link=request.form['website_link']
  newArtist.seeking_venue=True if 'seeking_venue' in request.form else False
  newArtist.seeking_description=request.form['seeking_description']

  try:
  
    db.session.add(newArtist)
    db.session.commit()
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:

    db.session.rollback()
    print(sys.exc_info())
    # DONE: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  finally:
    db.session.close()
  return redirect(url_for('index'))
  # on successful db insert, flash success
 
  # DONE: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
 


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # Done: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  ShowsData = db.session.query(Show).join(Artist).join(Venue).all()
  Datalist=[]
  for show in ShowsData: 
    Datalist.append({
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "artist_id": show.artist_id,
      "artist_name": show.artist.name, 
      "artist_image_link": show.artist.image_link,
      "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
    })

  return render_template('pages/shows.html', shows=Datalist)

  

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # DONE: insert form data as a new Show record in the db, instead
  newShow= Show()
  newShow.artist_id=request.form['artist_id']
  newShow.venue_id=request.form['venue_id']
  newShow.start_time=request.form['start_time']
  try:
      db.session.add(newShow)
      db.session.commit()
      flash('Show was successfully listed!')
  except :
     db.session.rollback()
     print(sys.exc_info())

     flash('An error occurred. Show could not be listed.')
  
  # DONE: on unsuccessful db insert, flash an error instead.
  
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
