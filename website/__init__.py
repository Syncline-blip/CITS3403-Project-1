from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_socketio import SocketIO
db = SQLAlchemy()
DB_NAME = "database.db"
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'abcd'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    socketio.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Messages

    create_database(app)
    with app.app_context():
        db.create_all()
        print('DB already exits')

    login_manager = LoginManager()
    # where to redirect if user is not logged in
    login_manager.login_view = 'views.intro'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# if database does not exist then create database
def create_database(app):
    with app.app_context():
        if not path.exists('./instance/' + DB_NAME):
            # create all tables if the messages table does not exist
            db.create_all()
            print('Created Database!')
            from .models import Room
            GLOB = Room(name='GLOB', description='Global chat room')
            ANON = Room(name='ANON', description='Anonymous chat room')
            SUPP = Room(name='SUPP', description='Support chat room')
            db.session.add(GLOB)
            db.session.add(ANON)
            db.session.add(SUPP)
            db.session.commit()
        else:
            print('Database already exists')