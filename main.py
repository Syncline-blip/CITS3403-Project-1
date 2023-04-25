from website import create_app, socketio
from website.sockets import connect, disconnect, message

app = create_app()


# I dont think we need below but leaving just incase for now
'''socketio.on_event("connect", connect)
socketio.on_event("disconnect", disconnect)
socketio.on_event("new-message", message)'''


if __name__ == '__main__':
    socketio.run(app,debug=True) 