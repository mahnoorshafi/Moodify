import json
import requests
import sys
import base64
import urllib
from settings import *
from flask import request, flash, session
from model import User, Track, Playlist, playlistTrack, db, connect_to_db

def get_user_authorization():
    """ User Authorization """

    url_args = '&'.join(['{}={}'.format(key,urllib.parse.quote(val)) for key,val in auth_query_parameters.items()])
    auth_url = '{}/?{}'.format(SPOTIFY_AUTH_URL, url_args)
    return auth_url


def get_tokens():
    """ Return authorization tokens from Spotify """

    # Request refresh and access tokens
    auth_token = request.args['code']

    code_payload = {
        'grant_type': 'authorization_code',
        'code': str(auth_token),
        'redirect_uri': REDIRECT_URI
    }

    base64encoded = base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode('ascii'))
    headers = {'Authorization': 'Basic {}'.format(base64encoded.decode('ascii'))}

    try: 
        post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    except:
        # Some error with *your* request, not Spotify
        current_app.logger.error("Spotify client failed")
        raise

    else:
        response_data = post_request.json()
        return response_data

    # Tokens that are Returned to Application
            # access_token = response_data['access_token']
            # refresh_token = response_data['refresh_token']
            # token_type = response_data['token_type']
            # expires_in = response_data['expires_in']


def get_auth_header(access_token):
    """ Return authorization header which will be used to access Spotify API """

    auth_header = {'Authorization': 'Bearer {}'.format(access_token)}
    return auth_header

def get_spotify_data(request, auth_header):
    """ Return data from Spotify get request """

    data = requests.get(request, headers = auth_header)

    if data.status_code == 200:
        data = data.json()

    elif data.status_code == 401:

        user = db.session.get(session.get('user'))
        user_refresh_token = user.refresh_token

        code_payload = {
            'grant_type': 'refresh_token',
            'refresh_token': user_refresh_token
        }

        base64encoded = base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode('ascii'))
        headers = {'Authorization': 'Basic {}'.format(base64encoded.decode('ascii'))}

        refresh_token_url = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)
        response_data = post_request.json()

        auth_header = {'Authorization': 'Bearer {}'.format(resonse_data['access_token'])}
        
        session['access_token'] = response_data['access_token']

        get_spotify_data(request, auth_header)

    return data


def post_spotify_data(request, auth_header):
    """ Return data from Spotify post request """

    data = requests.post(request, headers = auth_header)

    if data.status_code == 200:
        data = data.json()

    elif data.status_code == 401:

        user = db.session.get(session.get('user'))
        user_refresh_token = user.refresh_token

        code_payload = {
            'grant_type': 'refresh_token',
            'refresh_token': user_refresh_token
        }

        base64encoded = base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode('ascii'))
        headers = {'Authorization': 'Basic {}'.format(base64encoded.decode('ascii'))}

        refresh_token_url = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)
        response_data = post_request.json()

        auth_header = {'Authorization': 'Bearer {}'.format(resonse_data['access_token'])}
        
        session['access_token'] = response_data['access_token']

        get_spotify_data(request, auth_header)

    return data

def get_user_id(auth_header):
    """ Return users spotify id to add to database """ 

    request = f'{SPOTIFY_API_URL}/me'
    user_info_data = requests.get(request, headers=auth_header).json()
    user_id = user_info_data['id']

    return user_id





