import os 

# Client Keys
CLIENT_ID=os.environ['SPOTIFY_CLIENT_ID']
CLIENT_SECRET=os.environ['SPOTIFY_CLIENT_SECRET']
REDIRECT_URI=os.environ['SPOTIFY_REDIRECT_URI']

SCOPE='user-top-read user-library-read user-follow-read playlist-modify-public'

# Spotify URL
SPOTIFY_AUTH_URL='https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL='https://accounts.spotify.com/api/token'
SPOTIFY_API_BASE_URL='https://api.spotify.com'
API_VERSION='v1'
SPOTIFY_API_URL='{}/{}'.format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server-side Parameters
CLIENT_SIDE_URL='http://127.0.0.1'
PORT=5000

auth_query_parameters = {
    'response_type': 'code',
    'redirect_uri': REDIRECT_URI,
    'scope': SCOPE,
    'client_id': CLIENT_ID
}
