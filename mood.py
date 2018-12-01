import json
import requests
from random import shuffle
from spotify import *
from settings import *
from model import User, Track, Playlist, UserTrack, playlistTrack, db, connect_to_db
from scipy import stats 
import numpy as np


def get_top_artists(auth_header, num_entities):
    """ Return list of new user's top and followed artists """

    artists = []

    term = ['long_term', 'medium_term', 'short_term']

    for length in term:
        request = f'{SPOTIFY_API_URL}/me/top/artists?time_range={length}&limit={num_entities}'
        top_artists_data = requests.get(request, headers=auth_header).json()
        # top_artists_data = get_spotify_data(request, auth_header)
        top_artists = top_artists_data['items']
        for top_artist in top_artists:
            if top_artist['id'] not in artists:
                artists.append(top_artist['id'])

    users_followed_artists = f'{SPOTIFY_API_URL}/me/following?type=artist&limit={num_entities}'
    followed_artists_data = requests.get(users_followed_artists, headers=auth_header).json()
    # followed_artists_data = get_spotify_data(users_followed_artists, auth_header)

    followed_artists = followed_artists_data['artists']['items']

    for followed_artist in followed_artists:
        if followed_artist['id'] not in artists:
            artists.append(followed_artist['id'])

    return artists


def get_related_artists(auth_header, top_artists):
    """ Return list of related artists using users top artist """

    new_artists = []

    for artist_id in top_artists[:1]:
        request = f'{SPOTIFY_API_URL}/artists/{artist_id}/related-artists'
        related_artists_data = requests.get(request, headers=auth_header).json()
        # related_artists_data = get_spotify_data(request, auth_header)
        related_artists = related_artists_data['artists']

        for related_artist in related_artists:
            if related_artist['id'] not in new_artists:
                new_artists.append(related_artist['id'])

    artists = set(top_artists + new_artists)

    return list(artists)


def get_top_tracks(auth_header, artists):
    """ Get top tracks of artists """

    top_tracks = []

    for artist_id in artists:
        request = f'{SPOTIFY_API_URL}/artists/{artist_id}/top-tracks?country=US'
        track_data = requests.get(request, headers=auth_header).json()
        # track_data = get_spotify_data(request, auth_header)
        tracks = track_data['tracks']

        for track in tracks:
            if track['id'] not in top_tracks:
                top_tracks.append(track['id'])

    return top_tracks

def cluster_ids(tracks, n = 100):
    """ Return list of track ids clustered in groups of 100 """

    clustered_tracks = []
    for i in range(0, len(tracks), n):
        clustered_tracks.append(tracks[i:i + n])

    return clustered_tracks


def add_and_get_user_tracks(auth_header, clustered_tracks, mood):
    """ Add audio features of user's top tracks to database and return list of users track objects """

    track_audio_features = []

    for track_ids in clustered_tracks:
        ids = '%2C'.join(track_ids)
        request = f'{SPOTIFY_API_URL}/audio-features?ids={ids}'
        audio_features_data = requests.get(request, headers=auth_header).json()
        # audio_features_data = get_spotify_data(request, auth_header)
        audio_features = audio_features_data['audio_features']
        track_audio_features.append(audio_features)

    for tracks in track_audio_features:
        for track in tracks:
            track_id = track['id']
            track_uri = track['uri']
            track_valence = track['valence']
            track_danceability = track['danceability']
            track_energy = track['energy']

            track_exist = db.session.query(Track).filter(Track.id == track_id).all()

            if not track_exist:
                new_track = Track(id=track_id, 
                                uri=track_uri,
                                danceability=track_danceability, 
                                energy=track_energy, 
                                valence=track_valence)
                db.session.add(new_track)

            user = session.get('user')
            new_user_track_exist = db.session.query(UserTrack).filter(UserTrack.user_id == user, UserTrack.track_id == track_id).all()

            if not new_user_track_exist:
                new_user_track = UserTrack(user_id = user, track_id = track_id)
                db.session.add(new_user_track)
        db.session.commit()

    user_id = session.get('user')
    user = db.session.query(User).filter(User.id == user_id).one()
    user_tracks = user.tracks

    return user_tracks

def standardize_audio_features(user_tracks):
    """ Return dictionary of standardized audio features """

    user_tracks_valence = list(map(lambda track: track.valence, user_tracks))
    valence_array = np.array(user_tracks_valence)
    valence_zscores = stats.zscore(valence_array)
    valence_zscores = valence_zscores.astype(dtype=float).tolist()
    valence_cdf = stats.norm.cdf(valence_zscores)

    user_tracks_energy = list(map(lambda track: track.energy, user_tracks))
    energy_array = np.array(user_tracks_energy)
    energy_zscores = stats.zscore(energy_array)
    energy_zscores = energy_zscores.astype(dtype=float).tolist()
    energy_cdf = stats.norm.cdf(energy_zscores)

    user_tracks_danceability = list(map(lambda track: track.danceability, user_tracks))
    danceability_array = np.array(user_tracks_danceability)
    danceability_zscores = stats.zscore(danceability_array)
    danceability_zscores = danceability_zscores.astype(dtype=float).tolist()
    danceability_cdf = stats.norm.cdf(danceability_zscores)

    user_audio_features = {}

    for i, user_track in enumerate(user_tracks):
        user_audio_features[user_track.uri] = {'valence': valence_cdf[i], 
                                           'energy': energy_cdf[i], 
                                           'danceability': danceability_cdf[i]}
    
    return user_audio_features

def select_tracks(user_audio_features, mood):
    """ Return set of spotify track uri's to add to playlist """

    selected_tracks = []

    for track, feature in user_audio_features.items():
        if mood <= 0.10:
            if (0 <= feature['valence'] <= (mood + 0.15)) and (feature['energy'] <= (mood + 0.3)) and (feature['danceability'] <= (mood + 0.4)):
                selected_tracks.append(track)
        if mood <= 0.25:
            if ((mood - 0.1) <= feature['valence'] <= (mood + 0.05)) and (feature['energy'] <= (mood + 0.4)) and (feature['danceability'] <= (mood + 0.5)):
                selected_tracks.append(track)
        if mood <= 0.50:
            if ((mood - 0.1) <= feature['valence'] <= (mood + 0.05)) and (feature['energy'] <= (mood + 0.1)) and (feature['danceability'] <= mood):
                selected_tracks.append(track)
        if mood <= 0.75:
            if ((mood - 0.1) <= feature['valence'] <= (mood + 0.05)) and (feature['energy'] >= (mood - 0.1)) and (feature['danceability'] >= mood):
                selected_tracks.append(track)
        if mood <= 0.90:
            if ((mood - 0.1) <= feature['valence'] <= (mood + 0.05)) and (feature['energy'] >= (mood - 0.4)) and (feature['danceability'] >= (mood - 0.5)):
                selected_tracks.append(track)
        if mood <= 1.00:
            if ((mood - 0.15) <= feature['valence'] <= 1) and (feature['energy'] >= (mood - 0.3)) and (feature['danceability'] >= (mood - 0.4)):
                selected_tracks.append(track)

    shuffle(selected_tracks)
    playlist_tracks = selected_tracks[:36]
    
    return set(playlist_tracks)

def create_playlist(auth_header, user_id, playlist_tracks, mood):
    """ Creates playlist based on mood with selected tracks """

    mood_num = f'Mood {mood}'

    payload = { 
        'name' : mood_num,
        'description': 'Mood generated playlist'
        }

    playlist_request = f'{SPOTIFY_API_URL}/users/{user_id}/playlists'
    playlist_data = requests.post(playlist_request, data = json.dumps(payload), headers =auth_header).json()
    playlist_id = playlist_data['id']

    track_uris = '%2C'.join(playlist_tracks)
    add_tracks = f'{SPOTIFY_API_URL}/playlists/{playlist_id}/tracks?uris={track_uris}'
    tracks_added = requests.post(add_tracks, headers=auth_header).json()
    # tracks_added = post_spotify_data(add_tracks, auth_header)

    return playlist_data['external_urls']['spotify']








    
    




