from flask_socketio import join_room, leave_room, send, emit
from flask import session
from . import db, socketio
from .models import Messages, Room, User, ActiveMembers
from flask_login import current_user
from datetime import datetime

import random
import string

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

#Sends a Computer message to the current room
def computer_message(room,message):
    room_obj = Room.query.filter_by(room_name=room).first()

    computer = User.query.filter_by(id=1).first()
    date = datetime.now().strftime(DATE_FORMAT)
    content = {
        "username": computer.username,
        "profile_picture": computer.profile_picture,
        "message": message,
        "date": date
    }

    new_message = Messages(data=message, user_id=computer.id, room_id=room_obj.id,date=date)
    db.session.add(new_message)
    db.session.commit()

    send(content, to=room)

WORD_LIST = ['apple', 'banana', 'cherry', 'date', 'elder', 'fig']

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

    #Starts game
    if data["data"] == "./scramble":
        room_obj.game_mode = True  # Activate game mode
        room_obj.game_answer = random.choice(WORD_LIST)  # Assign a value to 'word'
        db.session.commit()
        scrambled_word = scramble_word(room_obj.game_answer)
        computer_message(room, "Unscramble this word: " + scrambled_word)
        return  # Exit the function after starting the game
    #if game mode is true
    if room_obj.game_mode:
        content = {
            "username": session.get("username"),
            "profile_picture": profile_picture,
            "message": data["data"],
            "date": date
        }

        new_message = Messages(data=data["data"], user_id=current_user.id, room_id=room_obj.id,date=date)
        db.session.add(new_message)
        db.session.commit()
        send(content, to=room)
        #if someone gets the correct word
        if data["data"] == room_obj.game_answer:
            
            winner_user = User.query.filter_by(username=session.get("username")).first()

            computer_message(room, f"{winner_user.username} is CORRECT, +5 points")

            winner_user.score = winner_user.score + 5
            room_obj.game_mode = False  # Reset game mode
            room_obj.game_answer = ""
            db.session.commit()
    else:
   
        print(room_obj.game_mode)

        #messages are now saved in the personal Messages Model
        new_message = Messages(data=data["data"], user_id=current_user.id, room_id=room_obj.id,date=date)
        db.session.add(new_message)
        db.session.commit()

        send(content, to=room)
        print(f"{session.get('username')} said: {data['data']}")
