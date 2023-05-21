from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash
import random

# Initializing SQLAlchemy instance
db = SQLAlchemy()

# Defining the database name
DB_NAME = "database.db"

# Initializing SocketIO instance
socketio = SocketIO()

# Initializing Migrate instance
migrate = Migrate()

def create_app(database_uri = f'sqlite:///{DB_NAME}'):
    # Create a Flask app
    app = Flask(__name__)
    
    # Configure the secret key and the database URI for the app
    app.config['SECRET_KEY'] = 'abcd'  # Should be a strong, unique key, not hardcoded in the code for security reasons
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    
    # Initialize the app for SQLAlchemy, Migrate, and SocketIO
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)

    # Import and register blueprints
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import models
    from .models import User

    # Create the database
    create_database(app)


    # Create all tables in the database
    with app.app_context():
        db.create_all()
        

    # Setup the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'views.intro'  # Redirect location if user is not logged in
    login_manager.init_app(app)

    # User loader callback for Flask-Login
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))  # Get the user by ID

    return app

# Function to create a database if it doesn't already exist
def create_database(app):
    with app.app_context():
        if not path.exists('./instance/' + DB_NAME):
            db.create_all()
            print('Created Database!')
            
            # Import models
            from .models import Room, User

            # Generate a random password for the computer 
            password = "".join(random.choices("erfijnfefecwdubewfodoi", k=10))
            # Creates the computer account
            computer = User(
                email="Computer@notreal", 
                username="CP", 
                password=generate_password_hash(password, method='sha256'), 
                score=0, 
                profile_picture="./static/images/ComputerProfilePic.png"
            )
            db.session.add(computer)

            #TODO below to be removed as just for testing purposes
            # for i in range(1, 21):
            #     email = f'user{i}@test.com'
            #     username = f'user{i}'
            #     password = f'password{i}'

            #     user = User(email=email, username=username, password=password,profile_picture="./static/images/ComputerProfilePic.png")
            #     db.session.add(user)

            db.session.commit()

            # Creates the three default general rooms
            GLOB = Room(room_name='GLOB', description='Global Chat Room')
            LFGG = Room(room_name='LFGG', description='Looking for Group Chat Room')
            SUPP = Room(room_name='SUPP', description='Support Chat Room')
            db.session.add(GLOB)
            db.session.add(LFGG)
            db.session.add(SUPP)
            
            # Commit the changes to the database
            db.session.commit()
        else:
            print('Database already exists')