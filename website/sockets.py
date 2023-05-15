from flask_socketio import join_room, leave_room, send, emit
from flask import session
from . import db, socketio
from .models import Messages, Room, User, ActiveMembers
from flask_login import current_user
from datetime import datetime
import re
import random
import string

DATE_FORMAT = "%H:%M:%S %d-%m-%Y"

general_rooms = ["GLOB", "LFGG", "SUPP"]





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
    if room_obj.game_mode == 1:
        gameMode = "ON"
    else:
        gameMode = "OFF"
    
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
        "all_member_profiles": profile_list,
        "gameMode" : gameMode
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

    #If room is in game mode and everyone leaves the game ends itself 
    active_members_count = ActiveMembers.query.filter_by(room_id=room_obj.id).count()
    if active_members_count == 0 and room_obj.game_mode != None:
        room_obj.game_mode = None
        room_obj.game_round = None
        room_obj.game_answer = None
        db.session.commit()
        computer_message(room,"No Active Users, Game Over")
        
    

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

    active_members_count = ActiveMembers.query.filter_by(room_id=room_obj.id).count()
    print(active_members_count)
    #if the message is the below command, and not one of the 3 general rooms or private room, a word scramble game starts
    match = re.search(r'\./scramble\s+(\w+)$', data["data"])
    if room_obj.game_mode is None and len(room_obj.room_name) == 4 and room_obj.room_name not in general_rooms:
        if match:
            #Game can only start when more then 1 person in the chat room
            word = match.group(1)
            '''if active_members_count == 1:
                computer_message(room,"Not enough members to start a game")'''
            
            if word == "fruit":
                # Do something for "./scramble" with "fruit"
                mode = 1
                start_scramble(room, room_obj, mode)
                return
            
            elif word == "videogames":
                # Do something for "./scramble" with "videogames"
                mode = 2
                start_scramble(room, room_obj, mode)
                return
            
            elif word == "css":
                # Do something for "./scramble" with "css"
                mode = 3
                start_scramble(room, room_obj, mode)
                return
            else:
                #computer_message(room,f"Scramble Category '{word}' is invalid.")
                computer_message(room,"Scramble KKKCategorys: fruit, videogames, css ")
        
    
        
    #if game_mode == 1 it means a word scramble game is being played
    if room_obj.game_mode in [1, 2, 3]:
        handle_scramble_mode(room_obj, data["data"], content, room)
    else:
        handle_normal_mode(room_obj, data["data"], content, room)





@socketio.on("scramble-timer-done")
def scramble_stop():
    room = session.get("room")
    room_obj = Room.query.filter_by(room_name=room).first()
    if room_obj.game_mode != None:
        room_obj.game_mode = None
        room_obj.game_round = None
        room_obj.game_answer = None
        db.session.commit()
        computer_message(room,"Timer Expired - No Winner")



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


#Scramble word function
def scramble_word(word):
    letters = list(word)
    random.shuffle(letters)
    return ''.join(letters)

#Kept short for demo purposes 
FRUIT_WORD_LIST = ['apple', 'banana', 'cherry', 'date', 'fig']
VIDEOGAME_TITLE_LIST = ['overwatch', 'pokemon', 'minecraft', 'fallout', 'fortnite', 'halo', 'skyrim']
CSS_TAG_LIST = ['body', 'span', 'class', 'margin', 'padding', 'background-color']

def start_scramble(room,room_obj, mode):
    room_obj.game_mode = mode
    room_obj.game_round = 1

    if room_obj.game_mode == 1:
        word_list = FRUIT_WORD_LIST
    elif room_obj.game_mode == 2:
        word_list = VIDEOGAME_TITLE_LIST
    elif room_obj.game_mode == 3:
        word_list = CSS_TAG_LIST

    room_obj.game_answer = random.choice(word_list)
    db.session.commit()
    scrambled_word = scramble_word(room_obj.game_answer)
    computer_message(room, f"Round {room_obj.game_round}: Unscramble this word: {scrambled_word}")


def handle_scramble_mode(room_obj, user_input, content, room):
    content["message"] = user_input
    new_message = Messages(data=user_input, user_id=current_user.id, room_id=room_obj.id, date=content["date"])
    db.session.add(new_message)
    db.session.commit()
    send(content, to=room)

    if user_input == room_obj.game_answer:
        winner_user = User.query.filter_by(username=session.get("username")).first()
        computer_message(room, f"{user_input} is CORRECT! {winner_user.username}  received 1 point!")
        winner_user.score += 1

        if room_obj.game_round == 3:
            computer_message(room, "Game Over! All rounds completed.")
            room_obj.game_mode = None
            room_obj.game_round = None
            room_obj.game_answer = None
        else:
            room_obj.game_round += 1

            if room_obj.game_mode == 1:
                word_list = FRUIT_WORD_LIST
            elif room_obj.game_mode == 2:
                word_list = VIDEOGAME_TITLE_LIST
            elif room_obj.game_mode == 3:
                word_list = CSS_TAG_LIST

            room_obj.game_answer = random.choice(word_list)
            scrambled_word = scramble_word(room_obj.game_answer)
            computer_message(room, f"Round {room_obj.game_round}: Unscramble this word: {scrambled_word}")
        
        db.session.commit()
    

#How a room acts when not in game mode
def handle_normal_mode(room_obj, user_input, content, room):
    print(room_obj.game_mode)
    new_message = Messages(data=user_input, user_id=current_user.id, room_id=room_obj.id, date=content["date"])
    db.session.add(new_message)
    db.session.commit()
    send(content, to=room)
    print(f"{session.get('username')} said: {user_input}")