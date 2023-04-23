from website import create_app
from flask_socketio import SocketIO, join_room, leave_room, send
from flask import Flask, render_template, request, session, redirect, url_for
import random
from string import ascii_uppercase
from flask_login import login_user, login_required, logout_user, current_user

app = create_app()
socketio = SocketIO(app)
rooms = {}
rooms["GLOB"] = {"members": 0, "messages": []} #Initialises room GLOB for global chat - always exists.
rooms["ANON"] = {"members": 0, "messages": []} #Initialises room ANON for anonymous chat - always exists.
rooms["SUPP"] = {"members": 0, "messages": []} #Initialises room SUPP for support chat - always exists.

def genCode(Length):
    while True:
        code = ''
        for _ in range(Length):
            code += random.choice(ascii_uppercase)
        
        if code not in rooms:
            break
    
    return code


@app.route("/home", methods=["POST", "GET"])
def home():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)
        globalChat = request.form.get("globalChat", False)
        anonChat = request.form.get("anonChat", False)
        supportChat = request.form.get("supportChat", False)

        #If We allow custom usernames we need this check.
        #if not name:
        #    return render_template("home.html", error="Please enter a name.", code=code, name=name)
        
        if join != False and not code:
            print("I AM HEREEEE")
            return render_template("home.html", error="Please enter a room code.", code=code, name=name)
        
       
        if globalChat != False:
            session["room"] = "GLOB"
            session["name"] = name
            return redirect(url_for("room"))
        elif anonChat != False:
            session["room"] = "ANON"
            session["name"] = "Anonymous"
            return redirect(url_for("room"))
        elif supportChat != False:
            session["room"] = "SUPP"
            session["name"] = name
            return redirect(url_for("room"))

        room = code
        if create != False:
            room = genCode(4)
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms:
            print("I am here so it's interesting...")
            return render_template("home.html", error="Room does not exist", code=code, name=name)

        #temporary data
        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("home.html")


@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

                                                  #Loads the Messages on load
    return render_template("room.html", code=room, mesasges=rooms[room]["messages"], user=current_user)

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
    app.run(debug=True) 