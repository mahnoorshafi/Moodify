import requests
import spotify
import mood
from settings import *
from model import User, Track, Playlist, UserTrack, playlistTrack, db, connect_to_db

from flask import Flask, request, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined

app = Flask(__name__)

app.jinja_env.undefinded = StrictUndefined

@app.route('/')
def homepage():
    """ Render welcome page with login button """

    if session.get('access_token'):
        return render_template('mood.html')

    else:
        return render_template('homepage.html')

@app.route('/spotify-auth')
def authorization():
    """ Spotify Authorization Page """

    auth_url = spotify.get_user_authorization()
    return redirect(auth_url)

@app.route('/mood')
def get_user_mood():
    """ Get user's current mood"""

    response_data = spotify.get_tokens()

    session['access_token'] = response_data['access_token']
    auth_header = spotify.get_auth_header(session.get('access_token'))

    username = spotify.get_user_id(auth_header)
    session['user'] = username 

    user = db.session.query(User).filter(User.id == username).all()

    if not user:
        new_user = User(id = username, refresh_token = response_data['refresh_token'])
        db.session.add(new_user)
        db.session.commit()

    # gathering users top artists
    top_artists = mood.get_top_artists(auth_header, 50)
    artists = mood.get_related_artists(auth_header, top_artists)

    session['artists'] = artists

    return render_template('mood.html')

@app.route('/playlist')
def playlist():
    """ Take user to spotify web player with created playlist """

    auth_header = spotify.get_auth_header(session.get('access_token'))

    user_mood = request.args.get('mood')

    username = session.get('user')

    user = db.session.query(User).filter(User.id == username).one()
    user_tracks = user.tracks

    if user_tracks:
        old_user_audio_feat = mood.standardize_audio_features(user_tracks)
        old_user_playlist_tracks = mood.select_tracks(old_user_audio_feat, float(user_mood))
        play = mood.create_playlist(auth_header, username, old_user_playlist_tracks, user_mood)
    else:
        user_artists = session.get('artists')
        new_user_top_tracks = mood.get_top_tracks(auth_header, user_artists)
        cluster = mood.cluster_ids(top_tracks)
        new_user_tracks = mood.add_and_get_user_tracks(auth_header, cluster, float(user_mood))
        new_user_playlist_tracks = mood.standardize_audio_features(new_user_tracks, float(user_mood))
        play = mood.create_playlist(auth_header, username, new_user_playlist_tracks, user_mood)

    return render_template('playlist.html', play = play)

