""" Models and database function for ***** """

from flask import Flask
from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

class User(db.Model):
    """ User Information"""

    __tablename__ = 'users'

    id = db.Column(db.String, primary_key=True, nullable=False)
    refresh_token = db.Column(db.String, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User id={self.id}>"

class Track(db.Model):
    """ Song Information """

    __tablename__ = 'tracks'

    id = db.Column(db.String, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    danceability = db.Column(db.Numeric(4,3), nullable=False)
    energy = db.Column(db.Numeric(4,3), nullable=False)
    valence = db.Column(db.Numeric(4,3), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Track id={self.id} title={self.name}>"


class Playlist(db.Model):
    """ Playlist Information """

    __tablename__ = 'playlists'

    id = db.Column(db.String, primary_key=True, nullable = False)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    mood = db.Column(db.Numeric(4,3), nullable=False)

    user = db.relationship('User', backref = 'playlists')
    tracks = db.relationship('Track', secondary='playlist_track')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Playlist id={self.id} user={self.user_id} mood={self.mood}>"


playlistTrack = db.Table('playlist_track',
        db.Column('playlist_id', db.String, db.ForeignKey('playlists.id'), nullable=False),
        db.Column('track_id', db.String, db.ForeignKey('tracks.id'), nullable=False)
    )

def connect_to_db(app):
    """Connect the database to app."""

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hb_project'
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # For interactive mode

    from server import app
    connect_to_db(app)
    db.create_all()
    print("Connected to DB.")
