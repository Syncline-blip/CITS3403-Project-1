from . import db
from flask_login import UserMixin
from datetime import datetime



# Room Model
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)                                                            # Room ID
    room_name = db.Column(db.String(50), nullable=False)                                                    # Room name
    description = db.Column(db.String(255))                                                                 # Room description
    created_at = db.Column(db.DateTime, server_default=db.func.now())                                       # Timestamp for when the room was created
    game_mode = db.Column(db.Integer)                                                                       # Game mode 
    game_round = db.Column(db.Integer)                                                                      # Game round 
    game_answer = db.Column(db.String(50))                                                                  # Game answer 
    messages = db.relationship('Messages', backref='room', lazy=True)                                       # Relation to messages in the room
    members = db.relationship('User', secondary='room_members', backref=db.backref('rooms', lazy=True))     # ManyToMany relation to users in the room


# RoomMembers Model for permanent members of private message rooms
class RoomMembers(db.Model):
    __tablename__ = 'room_members'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)                             # User ID
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), primary_key=True)                             # Room ID


# ActiveMembers Model for temporary active members in group chats
class ActiveMembers(db.Model):
    member = db.Column(db.Integer, primary_key=True)                                                        # Member ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))                                               # User ID
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))                                               # Room ID


# Messages Model
class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)                                                            # Message ID
    data = db.Column(db.String(10000))                                                                      # Message content
    date = db.Column(db.String(19), default=datetime.utcnow().strftime("%H:%M:%S %d-%m-%Y"))                # Timestamp for when the message was sent
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))                                               # ID of the user who sent the message
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))                                               # ID of the room where the message was sent

# Relationship for followers
followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),                        # Follower user ID
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))                         # Followed user ID
                     )


# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)                                                            # User ID
    email = db.Column(db.String(150), unique=True)                                                          # User email
    password = db.Column(db.String(150))                                                                    # User password
    username = db.Column(db.String(15), unique=True)                                                        # Username
    Messages = db.relationship('Messages')                                                                  # Relation to messages sent by the user
    score = db.Column(db.Integer)                                                                           # User score
    profile_picture = db.Column(db.String())                                                                # User profile picture
    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')                                                              # Relationship for followers