# Moodify

Moodify is a web application that uses the Spotify API to generate playlists based on a users Spotify listening history and current mood.

## Table of Contents
* [Overview](#overview)<br/>
* [Tech Stack](#techstack)<br/>
* [Setup/Installation](#installation)<br/>
* [Demo](#demo)<br/>
* [Future Features](#future)

<a name="overview"/></a>
## Overview
Once authorized, Moodify gathers and stores a users listening history in a PostgreSQL database along with information for three audio features: danceability, energy, and valence. In order to uniformly segment the data provided by Spotify, Moodify normalizes the audio feature data for each user and an algorithm is applied to the normalized values to create a playlist with tracks specific to the user and their current mood. Once the playlist is created, the users can then view and play their playlist through Spotify as well as Moodify itself.

<a name="techstack"/></a>
## Tech Stack
**Frontend:** ReactJS, Javascript, Jinja, jQuery, Bootstrap</br>
**Backend:** Python, Flask, SQLAlchemy, PostgreSQL<br/>
**Libraries:** Scipy, Numpy<br/>
**APIs:** Spotify<br/>

<a name="installation"/></a>
## Setup/Installation
Get Client ID and Client Secret from [Spotify](https://developer.spotify.com/) and save them to a file `secrets.sh`:
```
export SPOTIFY_CLIENT_SECRET=YOUR_KEY
export SPOTIFY_CLIENT_ID=YOUR_KEY
```
On local machine, go to directory where you want to work and clone Moodify repository:
```
$ git clone https://github.com/mahnoorshafi/Moodify.git
```
Create a virtual environment in the directory:
```
$ virtualenv env
```
Activate virtual environment:
```
$ source env/bin/activate
```
Install dependencies:
```
$ pip install -r requirements.txt
```
Create database:
```
$ createdb moodify
```
Create your database tables:
```
$ python3 model.py
```
Source secrets.sh:
```
$ source secrets.sh
```
Run the app:
```
$ python3 server.py
```
Open localhost:5000 on browser.

<a name="demo"/></a>
## Demo
**Log in through Spotify and create your playlist by selecting a mood:**
<br/><br/>
![Homepage](/static/images/readme/homepage.gif)
<br/>

**Once created, play your playlist through Spotify Web Player or through Moodify:**
<br/><br/>
![Selecting Mood](/static/images/readme/created.gif)
<br/>

**View playlist and select song to play as well as skip through songs:**
<br/><br/>
![View and Play Playlist](/static/images/readme/playlist-player.gif)
<br/>

<a name="features"/></a>
## Future Features
* Fine tune algorithm that selects songs
* Give user's the ability to view all their past mood playlists
* Option to preview playlist and then save it