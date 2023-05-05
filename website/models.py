from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime



class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    messages = db.relationship('Messages', backref='room', lazy=True)
    # Define a ManyToMany relationship between Room and User models
    members = db.relationship('User', secondary='room_members',
                              backref=db.backref('rooms', lazy=True))


class RoomMembers(db.Model):
    __tablename__ = 'room_members'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), primary_key=True)

class Members(db.Model):
    member = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    # func.now gets current date/time
    date = db.Column(db.String(19), default=datetime.utcnow().strftime("%H:%M:%S %d-%m-%Y"))
    # stores id of user who posted Messages
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))


followers = db.Table('followers',
                     db.Column('follower_id', db.Integer,
                               db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer,
                               db.ForeignKey('user.id'))
                     )


# Below is schema for user database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(15), unique=True)
    Messages = db.relationship('Messages')
    score = db.Column(db.Integer)
    profile_picture = db.Column(db.String())
    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')
