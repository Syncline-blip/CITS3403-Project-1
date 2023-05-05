from website import create_app, socketio
from website.sockets import connect, disconnect, message

app = create_app()

if __name__ == '__main__':
    socketio.run(app,debug=True) 