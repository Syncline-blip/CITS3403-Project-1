from flask_socketio import join_room, leave_room, send, emit
from flask import session
from . import db, socketio
from .models import Messages, Room, User
from flask_login import current_user
from datetime import datetime

DATE_FORMAT = "%H:%M:%S %d-%m-%Y"

@socketio.on("connect")
def connect():
    room = session.get("room")
    username = session.get("username") 
    if not room or not username:
        return
    room_obj = Room.query.filter_by(room_name=room).first()
    if not room_obj:
        leave_room(room)
        return
    
    user_obj = User.query.filter_by(username=username).first()
    profile_picture = user_obj.profile_picture if user_obj else None
    date = datetime.now()
    content = {
        "username": username,
        "profile_picture": profile_picture,
        "message": "has entered the room",
        "date": date.strftime(DATE_FORMAT)
    }
    join_room(room)
    send(content, to=room)  # Send the message to all users in the room
    print(f"{username} joined room {room}")


@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    username = session.get("username")
    user_obj = User.query.filter_by(username=username).first()
    profile_picture = user_obj.profile_picture if user_obj else None
    date = datetime.now()
    content = {
        "username": username,
        "profile_picture": profile_picture,
        "message": "has left the room",
        "date": date.strftime(DATE_FORMAT)
    }
    leave_room(room)

    send(content, to=room)
    print(f"{username} has left the room {room}")

@socketio.on("new-message")
def message(data):
    room = session.get("room")
    room_obj = Room.query.filter_by(room_name=room).first()
    if not room_obj:
        return

    user_obj = User.query.filter_by(username=session.get("username")).first()
    profile_picture = user_obj.profile_picture if user_obj else None
    date = datetime.now().strftime(DATE_FORMAT)

    content = {
        "username": session.get("username"),
        "profile_picture": profile_picture,
        "message": data["data"],
        "date": date
    }

    

    #messages are now saved in the personal Messages Model
    new_message = Messages(data=data["data"], user_id=current_user.id, room_id=room_obj.id,date=date)
    db.session.add(new_message)
    db.session.commit()

    send(content, to=room)
    print(f"{session.get('username')} said: {data['data']}")
