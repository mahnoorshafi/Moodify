import requests
import spotify
import mood
from settings import *

from flask import Flask, request, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined

app = Flask(__name__)

app.jinja_env.undefinded = StrictUndefined

# @app.route('/')
# def index():
#     """ Render page where user enters mood """

#     return render_template("index.html")

@app.route('/')
# @app.route('/spotify-auth')
def authorization():
    """ Spotify Authorization Page """

    auth_url = spotify.get_user_authorization()
    return redirect(auth_url)

@app.route('/callback')
def callback():

    response_data = spotify.get_tokens()
    auth_header = spotify.access_api(response_data)
    top_artists = mood.get_users_top_artists(auth_header, 50)
    artists = mood.get_related_artists(auth_header, top_artists)
    top_tracks = mood.get_top_tracks(auth_header, artists)

    return render_template('results.html', 
                            top_tracks = top_tracks)

