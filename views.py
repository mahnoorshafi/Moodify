import os
import json
import requests
import sys
import base64
import urllib
from settings import *

from flask import Flask, request, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined

app = Flask(__name__)


@app.route('/')
def index():
    # Auth Step 1: Authorization
    url_args = '&'.join(['{}={}'.format(key,urllib.parse.quote(val)) for key,val in auth_query_parameters.items()])
    auth_url = '{}/?{}'.format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)


@app.route('/callback')
def callback():
    # Auth Step 4: Requests refresh and access tokens
    auth_token = request.args['code']
    code_payload = {
        'grant_type': 'authorization_code',
        'code': str(auth_token),
        'redirect_uri': REDIRECT_URI
    }
    base64encoded = base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode('ascii'))
    headers = {'Authorization': 'Basic {}'.format(base64encoded.decode('ascii'))}
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    # Auth Step 5: Tokens are Returned to Application
    response_data = post_request.json()
    access_token = response_data['access_token']
    refresh_token = response_data['refresh_token']
    token_type = response_data['token_type']
    expires_in = response_data['expires_in']

    # Auth Step 6: Use the access token to access Spotify API
    authorization_header = {'Authorization': 'Bearer {}'.format(access_token)}

    # Get profile data
    user_profile_api_endpoint = f'{SPOTIFY_API_URL}/me'
    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    profile_data = json.loads(profile_response.text)

    # Combine profile and playlist data to display
    display_arr = [profile_data]
    return render_template('index.html',sorted_array=display_arr)

# @app.route("/playlists")