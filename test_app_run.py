# Run this to create a test data base

from website import create_app, socketio
from website.sockets import connect, disconnect, message

app = create_app("sqlite:///testing.db")
if __name__ == '__main__':
    socketio.run(app,debug=True) 