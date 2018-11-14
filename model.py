""" Models and database function for ***** """

from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

class User(db.Model):
    """ User Information"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    spotify_user_id = db.Column(db.Integer, nullable=False)
    refresh_token = db.Column(db.String, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User id={self.user_id}>"

class Track(db.Model):
    """ Song Information """

    __tablename__ = 'tracks'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    spotify_track_id = db.Column(db.String, nullable=False)
    track_name = db.Column(db.String, nullable=False)
    artist_id = db.Column(db.String, db.ForeignKey('artists.id'), nullable=False)
    danceability = db.Column(db.Numeric(4,3), nullable=False)
    energy = db.Column(db.Numeric(4,3), nullable=False)
    valence = db.Column(db.Numeric(4,3), nullable=False)

    artist = db.relationship('Artist', backref = 'tracks')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Track id={self.id} title={self.title} artist={self.artist}>"


class Playlist(db.Model):
    """ Playlist Information """

    __tablename__ = 'playlists'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mood = db.Column(db.Numeric(4,3), nullable=False)

    user = db.relationship('User', backref = 'playlists')
    tracks = db.relationship('Track', secondary='playlist_track')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Playlist id={self.id} user={self.user_id} mood={self.mood}>"

class Artist(db.Model):
    """ Artist Information """

    __tablename__ = 'artists'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    artist_name = db.Column(db.String, nullable=False)
    spotify_artist_id = db.Column(db.String, nullable=False)


    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Artist id={self.id} name={self.name} spotify id={self.spotify_artist_id}>"


class TopArtists(db.Model):
    """ Users top artists information """

    __tablename__ = 'top_artists'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref = 'topartists')
    artists = db.relationship('Artists', secondary='user_artists')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Top Artists id={self.id} user={self.user_id}>"


userArtists = db.Table('user_artists',
        db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False),
        db.Column('artist_id', db.String, db.ForeignKey('artists.id'),nullable=False)
    )


playlistTrack = db.Table('playlist_track',
        db.Column('playlist_id', db.Integer, db.ForeignKey('playlists.id'), nullable=False),
        db.Column('track_id', db.Integer, db.ForeignKey('tracks.id'), nullable=False)
    )


def connect_to_db(app):
    """Connect the database to app."""

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hb_project'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # For interactive mode

    from server import app
    connect_to_db(app)
    print("Connected to DB.")
