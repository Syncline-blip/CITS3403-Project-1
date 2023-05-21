from website import create_app, create_database, socketio
from website.sockets import connect, disconnect, message


app = create_app(testing=True)
if __name__ == '__main__':
    socketio.run(app,debug=True) 