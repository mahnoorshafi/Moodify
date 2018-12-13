# Moodify

Moodify is a web application that uses the Spotify API to generate mood-based playlists. Once authorized, Moodify gathers and stores a users listening history in a database along with information for three audio features: danceability, energy, and valence. In order to uniformly segment the data provided by Spotify, Moodify normalizes the audio feature data for each user and an algorithm is applied to the normalized values to create a playlist with tracks specific to the user and their current mood. Once the playlist is created, the users can then view and play their playlist through Spotify as well as Moodify itself.

![alt text](https://github.com/mahnoorshafi/Moodify/static/images/homepage.png)