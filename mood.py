import json
import requests
from settings import *
from pprint import pprint

def get_users_top_artists(auth_header, num_entities = 20):
    """ Return list of user's top and followed artists """

    artists = []

    term = ['short_term', 'medium_term', 'long_term']

    for length in term:
        request = f'{SPOTIFY_API_URL}/me/top/artists?time_range={length}&limit={num_entities}'
        top_artists_data = requests.get(request, headers=auth_header).json()
        top_artists = top_artists_data['items']
        for top_artist in top_artists:
            if top_artist['id'] not in artists:
                artists.append(top_artist['id'])

    users_followed_artists = f'{SPOTIFY_API_URL}/me/following?type=artist&limit={num_entities}'
    followed_artists_data = requests.get(users_followed_artists, headers=auth_header).json()

    followed_artists = followed_artists_data['artists']['items']

    for followed_artist in followed_artists:
        if followed_artist['id'] not in artists:
            artists.append(followed_artist['id'])

    return artists


def get_related_artists(auth_header, top_artists):
    """ Return list of related artists using users top 5 artists """

    new_artists = []

    for artist_id in top_artists[:6]:
        request = f'{SPOTIFY_API_URL}/artists/{artist_id}/related-artists'
        related_artists_data = requests.get(request, headers=auth_header).json()
        related_artists = related_artists_data['artists']

        for related_artist in related_artists:
            if related_artist['id'] not in new_artists:
                new_artists.append(related_artist['id'])

    artists = set(top_artists + new_artists)

    return artists

def get_top_tracks(auth_header, artists):
    """ Get top tracks of artists """

    top_tracks = []

    for artist_id in artists:
        request = f'{SPOTIFY_API_URL}/artists/{artist_id}/top-tracks?country=US'
        track_data = requests.get(request, headers=auth_header).json()
        tracks = track_data['tracks']

        for track in tracks:
            if (track['name'], track['id'], track['artists']) not in top_tracks:
                top_tracks.append((track['name'], track['id'], track['artists']))

    return top_tracks


def select_tracks(auth_header, tracks):
    """ Select tracks based om user's mood """

    selected_tracks = []

    




