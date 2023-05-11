from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_migrate import Migrate
import random
from werkzeug.security import generate_password_hash
db = SQLAlchemy()
DB_NAME = "database.db"
socketio = SocketIO()
migrate = Migrate()

def create_app(database_uri = f'sqlite:///{DB_NAME}'):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'abcd'
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    db.init_app(app)

    migrate.init_app(app, db)
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
            from .models import Room, User

            password = "".join(random.choices("erfijnfefecwdubewfodoi", k=10))
            Computer = User(email="Computer@notreal", username="CP", password=generate_password_hash(
            password, method='sha256'), score=0, profile_picture="./static/images/ComputerProfilePic.png")
            db.session.add(Computer)

            GLOB = Room(room_name='GLOB', description='Global Chat Room')
            LFGG = Room(room_name='LFGG', description='Looking for Group Chat Room')
            SUPP = Room(room_name='SUPP', description='Support Chat Room')
            db.session.add(GLOB)
            db.session.add(LFGG)
            db.session.add(SUPP)
            db.session.commit()
        else:
            print('Database already exists')