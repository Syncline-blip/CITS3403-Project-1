from flask_socketio import join_room, leave_room, send
from flask import session
from website.game_code import ( 
    computer_message, 
    handle_hangman, 
    handle_scramble_mode, 
    hangman_stop, 
    scramble_timer_done, 
    start_scramble, 
    startHangman
)
from . import db, socketio
from .models import Messages, Room, User, ActiveMembers
from flask_login import current_user
from datetime import datetime
import re


DATE_FORMAT = "%H:%M:%S %d-%m-%Y"
general_rooms = ["GLOB", "LFGG", "SUPP"]


# Socket.io event listener for when a client connects to the server
@socketio.on("connect")
def connect():
    # Retrieve room and username from session
    room = session.get("room")
    username = session.get("username") 
    if not room or not username:
        return

    # Query to find the room object with the same name
    room_obj = Room.query.filter_by(room_name=room).first()
    if not room_obj:
        # If room doesn't exist, leave room and return
        leave_room(room)
        return

    # Check the room's game mode
    gameMode = "ON" if room_obj.game_mode == 1 else "OFF"
    
    # Query to find the user object with the same username
    user_obj = User.query.filter_by(username=username).first()
    profile_picture = user_obj.profile_picture if user_obj else None

    # Get all active members in the room
    all_members = ActiveMembers.query.filter_by(room_id=room_obj.id).all()
    member_list = [x.user_id for x in all_members] #gets all users in the room atm
    username_list = []
    profile_list = []

    # Retrieve the username and profile picture of all active members
    for person in member_list:
        relevant_person = User.query.filter_by(id=person).first()
        username_list.append(relevant_person.username)
        profile_list.append(relevant_person.profile_picture)

    # Get current date and time
    date = datetime.now()

    # Create content dictionary
    content = {
        "username": username,
        "profile_picture": profile_picture,
        "message": "has joined the room.",
        "date": date.strftime(DATE_FORMAT),
        "all_member_usernames": username_list,
        "all_member_profiles": profile_list,
        "gameMode" : gameMode
    }

    # Create a new active member entry in the database
    new_member = ActiveMembers(user_id=current_user.id, room_id=room_obj.id)
    db.session.add(new_member)
    db.session.commit()

    # Join the room and send the content to the room
    join_room(room)
    send(content, to=room) #Sends a message - handled in room.html scripts.
    print(f"{username} joined room {room}")


@socketio.on("disconnect")
def disconnect():
    # Get room and username from session
    room = session.get("room")
    username = session.get("username")
    
    # Get user object and profile picture
    user_obj = User.query.filter_by(username=username).first()
    profile_picture = user_obj.profile_picture if user_obj else None
    
    # Get current date and time
    date = datetime.now()
    
    # Create content dictionary for sending the message
    content = {
        "username": username,
        "profile_picture": profile_picture,
        "message": "has left the room",
        "date": date.strftime(DATE_FORMAT),
        "disconnecting": "true"
    }
    
    # Leave the room
    leave_room(room)

    # Remove the user from the active members
    room_obj = Room.query.filter_by(room_name=room).first() 
    ActiveMembers.query.filter_by(user_id=current_user.id, room_id=room_obj.id).delete()
    db.session.commit()

    # If room is in game mode and everyone leaves, the game ends itself
    active_members_count = ActiveMembers.query.filter_by(room_id=room_obj.id).count()
    if active_members_count == 0 and room_obj.game_mode != None:
        room_obj.game_mode = None
        room_obj.game_round = None
        room_obj.game_answer = None
        db.session.commit()
        computer_message(room, "No Active Users, Game Over")
        
    # Send the content to the room
    send(content, to=room)
    print(f"{username} has left the room {room}")

@socketio.on("new-message")
def message(data):
    # Get room from session
    room = session.get("room")
    
    # Get room object
    room_obj = Room.query.filter_by(room_name=room).first()
    
    if not room_obj:
        return

    # Get user object and profile picture
    user_obj = User.query.filter_by(username=session.get("username")).first()
    profile_picture = user_obj.profile_picture if user_obj else None
    
    # Get current date and time
    date = datetime.now().strftime(DATE_FORMAT)

    # Create content dictionary for sending the message
    content = {
        "username": session.get("username"),
        "profile_picture": profile_picture,
        "message": data["data"],
        "date": date
    }

    # Get the count of active members in the room
    active_members_count = ActiveMembers.query.filter_by(room_id=room_obj.id).count()
    print(f"Members: {active_members_count}")
    
    # Check if the message is a command for starting a word scramble game
    bad_scramble_call = re.search(r'\./scramble\b', data["data"])
    scramble_command = re.search(r'\./scramble\s+(\w+)$', data["data"])
    hangman_command = re.search(r'\./hangman\b', data["data"])
    print(hangman_command)
    
    if room_obj.game_mode is None and len(room_obj.room_name) == 4 and room_obj.room_name not in general_rooms:
        if scramble_command:
            # Game can only start when more than 1 person in the chat room
            word = scramble_command.group(1)
            
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
                computer_message(room, f"Scramble Category '{word}' is invalid.")
            
        elif hangman_command:
            mode = 10
            startHangman(room, room_obj, mode)
        elif bad_scramble_call:
            computer_message(room, "Scramble call requires a category. Example: './scramble fruit'. Categories are: fruit, videogames and css")
        
    # If game_mode == 1 it means a word scramble game is being played
    if room_obj.game_mode in [1, 2, 3]:
        handle_scramble_mode(room_obj, data["data"], content, room)
    elif room_obj.game_mode == 10:
        handle_hangman(room_obj, data["data"], content, room)
    else:
        handle_normal_mode(room_obj, data["data"], content, room)

# How a room acts when not in game mode
def handle_normal_mode(room_obj, user_input, content, room):
    new_message = Messages(data=user_input, user_id=current_user.id, room_id=room_obj.id, date=content["date"])
    db.session.add(new_message)
    db.session.commit()
    send(content, to=room)
    print(f"{session.get('username')} said: {user_input}")


@socketio.on("timer-done")
def scramble_stop():
    # Get room from session
    room = session.get("room")
    
    # Get room object
    room_obj = Room.query.filter_by(room_name=room).first()
    
    if room_obj.game_mode != None:
        if room_obj.game_mode < 10:
            scramble_timer_done(room, room_obj)
        else:
            hangman_stop(room, room_obj)

