from flask_socketio import join_room, leave_room, send, emit
from flask import session
from . import db, socketio
from .models import Messages, Room, User, ActiveMembers
from flask_login import current_user
from datetime import datetime

import random
import string

DATE_FORMAT = "%H:%M:%S %d-%m-%Y"
WORD_LIST = ['apple', 'banana', 'cherry', 'date', 'elderberry', 'fig']




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
    all_members = ActiveMembers.query.filter_by(room_id=room_obj.id).all()
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
        "date": date.strftime(DATE_FORMAT),
        "all_member_usernames": username_list,
        "all_member_profiles": profile_list
    }
    
    new_member = ActiveMembers(user_id=current_user.id, room_id=room_obj.id)
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
        "date": date.strftime(DATE_FORMAT),
        "disconnecting": "true"
        }
    leave_room(room)

    room_obj = Room.query.filter_by(room_name=room).first() 
    ActiveMembers.query.filter_by(user_id=current_user.id, room_id=room_obj.id).delete()
    db.session.commit()

    send(content, to=room)
    print(f"{username} has left the room {room}")




# Define the function to scramble a word
def scramble_word(word):
    letters = list(word)
    random.shuffle(letters)
    return ''.join(letters)

# Define the function to handle the /scramble command
def handle_scramble_command(room):
    # Select a random word from the list of words
    word = random.choice(WORD_LIST)
    # Scramble the word
    scrambled_word = scramble_word(word)
    # Emit a message to all users in the room with the scrambled word
    profile_picture = './static/images/ComputerProfilePic.png'
    date = datetime.now().strftime(DATE_FORMAT)
    content = {
        "username": "CP",
        "profile_picture": profile_picture,
        "message": scrambled_word,
        "date": date
    }
    send(content, to=room)
    #emit('message', f"Unscramble this word: {scrambled_word}", room=session.get("room"))







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

    # Check if the message is a command
    if data["data"].startswith("./"):
        # Parse the command
        command = data["data"].split()[0]
        if command == "./s":
            # Handle the /scramble command
            handle_scramble_command(room)
            return
    

    #messages are now saved in the personal Messages Model
    new_message = Messages(data=data["data"], user_id=current_user.id, room_id=room_obj.id,date=date)
    db.session.add(new_message)
    db.session.commit()

    send(content, to=room)
    print(f"{session.get('username')} said: {data['data']}")
