import requests
import spotify
import mood
from settings import *
from model import User, Track, Playlist, playlistTrack, db, connect_to_db

from flask import Flask, request, redirect, render_template, flash, session
from sqlalchemy.sql import exists 
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined

app = Flask(__name__)

app.jinja_env.undefinded = StrictUndefined

@app.route('/')
def homepage():
    """ Render welcome page with login button """

    return render_template('homepage.html')

@app.route('/spotify-auth')
def authorization():
    """ Spotify Authorization Page """

    auth_url = spotify.get_user_authorization()
    return redirect(auth_url)

@app.route('/callback')
def get_user_tokens():
    """ Get user's authorization header and artists"""

    response_data = spotify.get_tokens()
    auth_header = spotify.access_api(response_data)

    user_id = spotify.get_user_id(auth_header)

    session['user'] = user_id 
    session['access_token'] = response_data['access_token']

    user_exist = db.session.query(exists().where(User.id == user_id))

    if not user_exist:
        new_user = User(id = user_id, refresh_token = response_data['refresh_token'])
        db.session.add(new_user)
        db.session.commit()

    top_artists = mood.get_top_artists(auth_header, 20)
    artists = mood.get_related_artists(auth_header, top_artists)

    app.logger.info(artists)

    return render_template('mood.html')

@app.route('/playlist')
def playlist():
    """ Take user to spotify web player with created playlist """

    response_data = spotify.get_tokens()
    auth_header = spotify.access_api(response_data)

    top_tracks = mood.get_top_tracks(auth_header, artists)
    cluster = mood.cluster_ids(top_tracks)
    select = mood.select_tracks(auth_header, cluster, 1.00)

    return render_template('results.html',
                             select = select)

