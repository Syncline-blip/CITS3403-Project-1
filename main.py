from website import create_app, socketio
from flask_socketio import SocketIO, join_room, leave_room, send
from flask import Flask, render_template, request, session, redirect, url_for
import random
from string import ascii_uppercase
from flask_login import login_user, login_required, logout_user, current_user
from website.constants import rooms

app = create_app()


@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"]+= 1
    print(f"{name} joined room {room}")


@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        #if rooms[room]["members"] <= 0:
        #    del rooms[room]
    

    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")


@socketio.on("new-message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return
    
    content = {
        "name":  session.get("name"),
        "message": data["data"]
        #Date & time of sent message should be here and parsed.
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")



if __name__ == '__main__':
    socketio.run(app,debug=True) 