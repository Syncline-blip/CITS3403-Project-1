from flask_socketio import join_room, leave_room, send
from flask import session
from . import db, socketio
from .models import Messages, Room, User, Members
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
    all_members = Members.query.filter_by(room_id=room_obj.id).all()
    member_list = [x.user_id for x in all_members] #gets all users in the room atm
    username_list = []
    profile_list = []

    for person in member_list:
        relevant_person = User.query.filter_by(id=person).first()
        username_list.append(relevant_person.username)
        profile_list.append(relevant_person.profile_picture)


    date = datetime.now()
    content = {
        "username": username,
        "profile_picture": profile_picture,
        "message": "has joined the room.",
        "date": date.strftime("%H:%M:%S %d-%m-%Y"),
        "all_member_usernames": username_list,
        "all_member_profiles": profile_list
    }
    
    new_member = Members(user_id=current_user.id, room_id=room_obj.id)
    db.session.add(new_member)
    db.session.commit()

    join_room(room)
    send(content, to=room) #Sends a message - handled in room.html scripts.
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
        "date": date.strftime("%H:%M:%S %d-%m-%Y"),
        "disconnecting": "true"
    }
    leave_room(room)

    room_obj = Room.query.filter_by(room_name=room).first() 
    Members.query.filter_by(user_id=current_user.id, room_id=room_obj.id).delete()
    db.session.commit()

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
