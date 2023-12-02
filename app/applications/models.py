from .database import db 

class User(db.Model):
    #defining the user table
    __tablename__ = 'user'
    #id = db.Column(db.Integer, , autoincrement=True)
    user_name = db.Column(db.String(120),nullable=False, primary_key=True)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.Text, nullable=False, default="user")
class Admin(db.Model):
    #defining the admin table
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(120),nullable=False)
     
    password = db.Column(db.Text, nullable=False)
    
class Music(db.Model):
    #defining the music table

    #__tablename__ = "musics"
    __tablename__ = "music_with_play_count"
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(),  unique=True) #for now removed nullable
    Genre = db.Column(db.String(), nullable=False)
    Artist = db.Column(db.String(),nullable=False)
    path = db.Column(db.String(),nullable=False, unique=True)
    play_count = db.Column(db.Integer, nullable=False, default=0)

class album(db.Model):

    __tablename__ = "creator"
    album_name = db.Column(db.String(),primary_key=True)
    artist = db.Column(db.String())
    song_name = db.Column(db.String())

class flag_user(db.Model):
    __tablename__ = 'flag_user'
    name = db.Column(db.String(), primary_key=True)
    flag = db.Column(db.String(), nullable=False)

class music_rating(db.Model):
    __tablename__ = "music_rating"
    song = db.Column(db.String(), primary_key=True)
    ratings = db.Column(db.String(), nullable=False)

class block_music(db.Model):
    __tablename__ = 'blocked_song'
    name = db.Column(db.String(), primary_key=True)
    status = db.Column(db.String(), nullable=False, default="Blacklisted")