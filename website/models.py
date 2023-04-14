from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    # func.now gets current date/time
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # stores id of user who posted Messages
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


# Below is schema for user database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    Messages = db.relationship('Messages')
    score = db.Column(db.Integer)
    image_file = db.Column(db.String())
    followed = db.relationship('User', 
                               secondary=followers, 
                               primaryjoin=(followers.c.follower_id == id), 
                               secondaryjoin=(followers.c.followed_id == id), 
                               backref=db.backref('followers', lazy='dynamic'), 
                               lazy='dynamic')
      
    
    
