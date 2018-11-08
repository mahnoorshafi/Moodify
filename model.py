""" Models and database function for ***** """

from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

class User(db.Model):
    """ User of Adjacency """

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User id={self.user_id}>"

class Song(db.Model):
    """ Song Information """

    __tablename__ = 'songs'

    song_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    artist = db.Column(db.String(64), nullable=False)
    danceability = db.Column(db.Numeric(4,3), nullable=False)
    energy = db.Column(db.Numeric(4,3), nullable=False)
    valence = db.Column(db.Numeric(4,3), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Song id={self.song_id} title={self.title} artist={self.artist}>"


class Playlist(db.Model):
    """ Playlist Information """

    __tablename__ = 'playlists'

    playlist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    mood = db.Column(db.Numeric(4,3), nullable=False)

    user = db.relationship('User', backref = 'playlist')
    songs = db.relationship('Song', secondary='playlist_song', backref = 'playlists')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Playlist id={self.playlist_id} user={self.user_id} mood={self.mood}>"


PlaylistSong = db.Table('playlist_song',
        db.Column('playlist_id', db.Integer, db.ForeignKey('playlists.playlist_id'), nullable=False),
        db.Column('song_id', db.Integer, db.ForeignKey('songs.song_id'), nullable=False)
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
