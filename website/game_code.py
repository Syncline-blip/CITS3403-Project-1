from flask_socketio import send
from flask import session
from . import db
from .models import Messages, Room, User, ActiveMembers
from flask_login import current_user
from datetime import datetime
import re
import random


DATE_FORMAT = "%H:%M:%S %d-%m-%Y"

general_rooms = ["GLOB", "LFGG", "SUPP"]
global word_string


HANGMAN_WORD_LIST = ["apple", "banana", "cat", "dog", "elephant", "flower", "guitar", "house", "island", "jungle"]

def startHangman(room, room_obj, mode):
    room_obj.game_mode = mode
    room_obj.game_round = 20  # Used to Indicate Lives.
    word = random.choice(HANGMAN_WORD_LIST)
    msg = '_' * len(word)
    room_obj.game_answer = word
    room_obj.current_guess = msg
    db.session.commit()
    string_with_space = ' '.join(list(msg))
    # computer_message(room, "Hangman Started! Work as a team to guess your letter in 5 lives! Oh, and watch out for that timer!")
    computer_message(room, "Hangman Started! Work as a team to guess your letter in 5 lives! Use ./v to guess the letter v")
    computer_message(room, f"{string_with_space}")


def handle_hangman(room_obj, user_input, content, room):
    content["message"] = user_input
    new_message = Messages(data=user_input, user_id=current_user.id, room_id=room_obj.id, date=content["date"])
    db.session.add(new_message)
    db.session.commit()
    send(content, to=room)

    stop_command = re.search(r'\./stop\b', user_input)
    if stop_command:
        if room_obj.game_mode != None:
            room_obj.game_mode = None
            room_obj.game_answer = None
            room_obj.game_round = None
            computer_message(room, "Hangman Stopped.")

    # Check if user_input starts with "./" and followed by a single character
    if user_input.startswith('./') and len(user_input) == 3:
        user_input = user_input[2:]  # Strip out "./"
        if user_input in room_obj.game_answer:
            out = modify_word_string(len(room_obj.game_answer), user_input, room_obj.current_guess, room_obj.game_answer)
            if room_obj.current_guess != out:
                room_obj.current_guess = out
                db.session.commit()
                if room_obj.current_guess == room_obj.game_answer:
                    room_obj.game_mode = None
                    db.session.commit()
                    computer_message(room, f"CORRECT! The word was '{room_obj.game_answer}'. All active members earned 2 points!")
                    # Gets the list of active members in the room in the database, and then matches using user_id to +2 points.
                    all_members = ActiveMembers.query.filter_by(room_id=room_obj.id).all()
                    for i in all_members:
                        person = User.query.filter_by(id=i.user_id).first()
                        person.score += 2
                        db.session.commit()

                else:
                    word_list = list(room_obj.current_guess)
                    spaced = ' '.join(word_list)
                    computer_message(room, f"{spaced}")

            else:
                computer_message(room, f"{user_input} has already been discovered in the word. No lives lost.")
        else:
            word_list = list(room_obj.current_guess)
            spaced = ' '.join(word_list)
            room_obj.game_round -= 1
            if room_obj.game_round <= 15:
                computer_message(room, f"Out of lives! The word was {room_obj.game_answer}.")
                room_obj.game_mode = None
                room_obj.game_round = None
                room_obj.game_answer = None
            else:
                computer_message(room, f"Letter '{user_input}' is not in the word")
                computer_message(room, f"{room_obj.game_round-15} lives remain...")
                computer_message(room, f"{spaced}")
            db.session.commit()


def modify_word_string(length, guess, current_word, answer):
    word_list = list(current_word)
    for i in range(length):
        if word_list[i] == "_" and answer[i] == guess:
            word_list[i] = guess

    word_list = ''.join(word_list)
    return word_list


# Sends a Computer message to the current room
def computer_message(room, message):
    room_obj = Room.query.filter_by(room_name=room).first()

    computer = User.query.filter_by(id=1).first()
    date = datetime.now().strftime(DATE_FORMAT)
    content = {
        "username": computer.username,
        "profile_picture": computer.profile_picture,
        "message": message,
        "date": date
    }

    new_message = Messages(data=message, user_id=computer.id, room_id=room_obj.id, date=date)
    db.session.add(new_message)
    db.session.commit()

    send(content, to=room)


# Scramble word function
def scramble_word(word):
    letters = list(word)
    random.shuffle(letters)
    return ''.join(letters)


# Kept short for demo purposes
FRUIT_WORD_LIST = ['apple', 'banana', 'cherry', 'date', 'fig']
VIDEOGAME_TITLE_LIST = ['overwatch', 'pokemon', 'minecraft', 'fallout', 'fortnite', 'halo', 'skyrim']
CSS_TAG_LIST = ['body', 'span', 'class', 'margin', 'padding', 'background-color']


def start_scramble(room, room_obj, mode):
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

    stop_command = re.search(r'\./stop\b', user_input)
    if stop_command:
        if room_obj.game_mode != None:
            room_obj.game_mode = None
            room_obj.game_answer = None
            room_obj.game_round = None
            computer_message(room, "Scramble Stopped.")

    if user_input == room_obj.game_answer:
        winner_user = User.query.filter_by(username=session.get("username")).first()
        computer_message(room, f"{user_input} is CORRECT! {winner_user.username} received 1 point!")
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


def scramble_timer_done(room, room_obj):

    if room_obj.game_mode == 1:
        word_list = FRUIT_WORD_LIST
    elif room_obj.game_mode == 2:
        word_list = VIDEOGAME_TITLE_LIST
    elif room_obj.game_mode == 3:
        word_list = CSS_TAG_LIST

    if room_obj.game_round == 1:
        room_obj.game_round = 2
        computer_message(room, f"Timer Expired! The word was {room_obj.game_answer}")
        room_obj.game_answer = random.choice(word_list)
        scrambled_word = scramble_word(room_obj.game_answer)
        computer_message(room, f"Round {room_obj.game_round}: Unscramble this word: {scrambled_word}")

    elif room_obj.game_round == 2:
        room_obj.game_round = 3
        computer_message(room, f"Timer Expired! The word was {room_obj.game_answer}")
        room_obj.game_answer = random.choice(word_list)
        scrambled_word = scramble_word(room_obj.game_answer)
        computer_message(room, f"Round {room_obj.game_round}: Unscramble this word: {scrambled_word}")

    elif room_obj.game_round == 3:
        computer_message(room, f"Timer Expired! Game Over! The final word was {room_obj.game_answer}")
        room_obj.game_mode = None
        room_obj.game_round = None
        room_obj.game_answer = None

    db.session.commit()


def hangman_stop(room, room_obj):
    computer_message(room, f"Timer Expired! Game Over! The word was {room_obj.game_answer}")
    room_obj.game_mode = None
    room_obj.game_round = None
    room_obj.game_answer = None
    db.session.commit()