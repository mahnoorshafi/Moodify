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
    top_artists = mood.get_top_artists(auth_header, 20)
    artists = mood.get_related_artists(auth_header, top_artists)
    top_tracks = mood.get_top_tracks(auth_header, artists)
    cluster = mood.cluster_ids(top_tracks)
    select = mood.select_tracks(auth_header, cluster, 1.00)

    return render_template('results.html',
                             select = select)

