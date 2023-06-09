from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, session
from sqlalchemy import not_
from .models import User, Messages, Room
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import uuid as uuid
from werkzeug.utils import secure_filename
import random
from string import ascii_uppercase
import os
import re



ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

auth = Blueprint('auth', __name__)

#Injects the current user into the template context.
@auth.app_context_processor
def inject_user():
    return dict(user=current_user)


def gencode(length):
    while True:
        code = ''
        for _ in range(length):
            code += random.choice(ascii_uppercase)

        room = Room.query.filter_by(room_name=code).first()
        if room is None:
            break

    return code


@auth.route("/home", methods=["POST", "GET"])
@login_required  # makes this page accessible only if user is logged in
def home():

    #Code for the favourite and members List
    #Excludes current_user and the Computer which has id 1
    favourite_list = current_user.followed.order_by(User.username).filter(User.id != current_user.id, User.id != 1)
    not_favourite_list = User.query.filter(not_(User.id.in_([user.id for user in current_user.followed])), User.id != 1).all()
    
    #Code for the leaderboard
    # Excludes the Computer(id=1) from the leaderboards
    num_users = db.session.query(User).filter(User.id != 1).count()

    top_three_scores = None
    if num_users > 3:
        # Gets the top three scores but excludes the user with id=1 and then changes the order from 1,2,3 to 2,1,3
        top_three_scores = User.query.filter(User.id != 1).order_by(User.score.desc()).limit(3).all()
        top_three_scores[1], top_three_scores[0], top_three_scores[2] = top_three_scores[0], top_three_scores[1], top_three_scores[2]
        # Gets all the other scores in descending order excluding the user with id=1
        other_scores = User.query.filter(User.id != 1).order_by(User.score.desc()).offset(3).all()
    else:
        # If the User count <= 3 we display all users in the table excluding the user with id=1
        other_scores = User.query.filter(User.id != 1).order_by(User.score.desc()).all()

    
    if request.method == "POST":
        username = current_user.username
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)
        globalChat = request.form.get("globalChat", False)
        lfgChat = request.form.get("lfgChat", False)
        supportChat = request.form.get("supportChat", False)

        private_message = request.form.get("private_message", False)
        chatter_id = request.form.get("chatter_id", False)
        chatter = User.query.get(chatter_id)
        

        # If We allow custom usernames we need this check.
        # if not name:
        #    return render_template("home.html", error="Please enter a name.", code=code, name=name)

        if join != False and not code or join != False and len(code) != 4:
            print("I AM HEREEEE")
            return render_template("home.html", error="Please enter a 4-letter room code", code=code, favourite_list=favourite_list, not_favourite_list=not_favourite_list,top_three_scores=top_three_scores, other_scores=other_scores, num_users=num_users)
        

        if private_message != False:
            # Check if a room already exists between current user and chatter
            existing_room = Room.query.filter(Room.members.any(id=current_user.id)).filter(Room.members.any(id=chatter.id)).first()
            if existing_room:
                session["room"] = existing_room.room_name
                session["username"] = username
                return redirect(url_for("auth.private_room"))
            else:
                # Create a new room if one does not exist
                new_room_name = gencode(6)
                new_room = Room(room_name=new_room_name, description="Private Chat Room")
                new_room.members.append(current_user)
                new_room.members.append(chatter)
                db.session.add(new_room)
                db.session.commit()

                session["room"] = new_room_name
                session["username"] = username
            return redirect(url_for("auth.private_room"))
        
        if globalChat != False:
            session["room"] = "GLOB"
            session["username"] = username
            return redirect(url_for("auth.room"))
        elif lfgChat != False:
            session["room"] = "LFGG"
            session["username"] = username
            return redirect(url_for("auth.room"))
        elif supportChat != False:
            session["room"] = "SUPP"
            session["username"] = username
            return redirect(url_for("auth.room"))

        new_room_name = code
        room = Room.query.filter_by(room_name=new_room_name).first()
        if create != False:
            new_room_name = gencode(4)
            new_room = Room(room_name=new_room_name, description=f'Custom Room {new_room_name}')
            db.session.add(new_room)
            db.session.commit()
        elif room is None:
            print("I am here so it's interesting...")
            return render_template("home.html", error="Room '" + code+"' does not exist", favourite_list=favourite_list, not_favourite_list=not_favourite_list,top_three_scores=top_three_scores, other_scores=other_scores, num_users=num_users)

        # temporary data
        session["room"] = new_room_name
        session["username"] = username

        #trying to enter a room thats in a game shows the error below.
        game_mode_value = Room.query.filter_by(room_name=new_room_name).value(Room.game_mode)
        if game_mode_value is not None:
            print("Game mode on so cant join")
            return render_template("home.html", error="Room '" + code+"' in game. Try again later", favourite_list=favourite_list, not_favourite_list=not_favourite_list,top_three_scores=top_three_scores, other_scores=other_scores, num_users=num_users)

        return redirect(url_for("auth.room"))

    return render_template("home.html",favourite_list=favourite_list, not_favourite_list=not_favourite_list,top_three_scores=top_three_scores, other_scores=other_scores, num_users=num_users)

@auth.route("/private_room")
@login_required
def private_room():
    current_room_name = session.get("room")
    username = session.get("username")

    if not current_room_name or not username:
        return redirect(url_for("auth.home"))
    
    room = Room.query.filter_by(room_name=current_room_name).first()
    if room is None:
        return redirect(url_for("auth.home"))

    # Load messages associated with this room
    messages = (
        db.session.query(Messages, User.username, User.profile_picture)
        .join(User, User.id == Messages.user_id)
        .filter(Messages.room_id == room.id)
        .all()
    )

    # Find the other user in the room
    other_user = next((member for member in room.members if member != current_user), None)

    return render_template("private_room.html", room=room, messages=messages,other_user=other_user)



@auth.route("/room")
@login_required
def room():
    current_room_name = session.get("room")
    username = session.get("username")

    if not current_room_name or not username:
        return redirect(url_for("auth.home"))
    
    room = Room.query.filter_by(room_name=current_room_name).first()
    if room is None:
        return redirect(url_for("auth.home"))

    # Load messages associated with this room
    messages = (
        db.session.query(Messages, User.username, User.profile_picture)
        .join(User, User.id == Messages.user_id)
        .filter(Messages.room_id == room.id)
        .all()
    )

    return render_template("room.html", room=room, messages=messages)


@auth.route('/search_messages')
def search_messages():
    # Get the value of the 'query' and 'room_id' parameters from the request's query string
    query = request.args.get('query')
    room_id = request.args.get('room_id')

    if not query:
        return ''

    # Check if the query starts with './from'
    search_by_user = query.startswith('./from')

    if search_by_user:
        # Remove './from' from the query and strip any leading/trailing spaces
        query = query.replace('./from', '').strip()

    # Query the database to retrieve messages, usernames, and profile pictures
    messages = db.session.query(Messages, User.username, User.profile_picture) \
        .join(User, Messages.user_id == User.id) \
        .filter(Messages.room_id == room_id)

    if search_by_user:
        # Filter messages by username
        messages = messages.filter(User.username.like(f'%{query}%'))
    else:
        # Filter messages by message content
        messages = messages.filter(Messages.data.like(f'%{query}%'))

    # Retrieve all the filtered messages from the database
    messages = messages.all()

    # Render the 'messages.html' template with the retrieved messages
    return render_template('messages.html', messages=messages)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Filter all users by the provided email and return the first result (assuming there's only one)
        user = User.query.filter_by(email=email).first()

        if user:
            # Check if the provided password matches the hashed password stored in the user object
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                # Remember that the user is logged in
                login_user(user, remember=True)
                return redirect(url_for('auth.home'))
            else:
                # Password provided does not match the user's password
                flash('Incorrect password, please try again', category='error')
        else:
            # No user with the provided email exists
            flash('Email does not exist.', category='error')

    # Render the login page with the current user (if logged in)
    return render_template("login.html")


@auth.route('/logout')
@login_required  # Makes this page accessible only if the user is logged in
def logout():
    logout_user()  # Log out the current user
    flash('Logged out successfully!', category='success')
    return redirect(url_for('auth.login'))  # Redirect to the login page


@auth.route('/add_favourite', methods=['GET', 'POST'])
@login_required
def add_favourite():
    user = current_user
    number = int(request.form.get('favourite_id'))
    favourite = User.query.filter_by(id=number).first()
    user.followed.append(favourite)
    db.session.commit()
    return redirect(url_for('auth.home'))


@auth.route('/remove_favourite', methods=['GET', 'POST'])
@login_required
def remove_favourite():
    user = current_user
    number = int(request.form.get('favourite_id'))
    favourite = User.query.filter_by(id=number).first()
    user.followed.remove(favourite)
    db.session.commit()
    return redirect(url_for('auth.home'))

# checks if the filenames extension is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@auth.route('/account', methods=['GET', 'POST'])
@login_required  # makes this page accessible only if user is logged in
def account():
    if request.method == 'POST':
        user = current_user

        new_email = request.form.get('email')
        new_username = request.form.get('username')
        new_password1 = request.form.get('password1')
        new_password2 = request.form.get('password2')
        
        
        if 'profile_picture' in request.files and request.files['profile_picture'].filename != '':
            img = request.files.get('profile_picture')
            if img and allowed_file(img.filename):
                # Get image name
                pic_filename = secure_filename(img.filename)
                # Set unique image name
                pic_name = str(uuid.uuid1()) + "_" + pic_filename
                # Save image
                img.save(os.path.join(current_app.root_path,
                        'static/images/profile_pictures', pic_name))
                # get image path
                pic_path = './static/images/profile_pictures/' + pic_name
            else:
                flash('Uploaded image must be a png, jpg or jpeg', category='error')
                return render_template("account.html")
        else:
            #if no image uploaded profile picture stays the same
            pic_path = user.profile_picture

        # check if email changing to already exists
        other_user = User.query.filter_by(email=new_email).first()
        other_user_username = User.query.filter_by(username=new_username).first()

        
        
        #if the email matches another user who is NOT the current user, email update fails
        if other_user and other_user.id != user.id:
            flash('Email already exists', category='error')
        #if the username matches another user who is NOT the current user, username update fails
        elif other_user_username and other_user_username.id != user.id:
            flash('Username already exists', category='error')
        elif new_email is not None and len(new_email) < 4 or len(new_email) > 150:
            flash('Email must be between 4 and 150 characters long', category='error')
        elif new_username is not None and len(new_username) < 2 or len(new_username) > 15:
            flash('Username must be between 2 and 15 characters long', category='error')
        elif new_password1 != new_password2:
            flash('Passwords must match', category='error')
        elif new_password1 == "" and new_password2 == "":
            user.email = new_email
            user.username = new_username
            user.profile_picture = pic_path
            db.session.commit()
            flash('Account Updated', category='success')
            return redirect(url_for('auth.home'))
        elif new_password1 is not None and not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{7,}$', new_password1):
            flash('Password must be at least 7 characters long and contain at least one letter, one number, and one special character', category='error')
        else:
    
            user.email = new_email
            user.username = new_username
            user.password = generate_password_hash(new_password1, method='sha256')
            user.profile_picture = pic_path
            db.session.commit()
            flash('Account Updated', category='success')
            return redirect(url_for('auth.home'))

    return render_template("account.html")


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if 'profile_picture' in request.files and request.files['profile_picture'].filename != '':
            img = request.files.get('profile_picture')
            if img and allowed_file(img.filename):
                # Get image name
                pic_filename = secure_filename(img.filename)
                # Set unique image name
                pic_name = str(uuid.uuid1()) + "_" + pic_filename
                # Save image
                img.save(os.path.join(current_app.root_path,
                        'static/images/profile_pictures', pic_name))
                # get image path
                pic_path = './static/images/profile_pictures/' + pic_name
            else:
                flash('Uploaded image must be a png, jpg or jpeg', category='error')
                return render_template("account.html")
        else:
            #if no image uploaded profile picture stays the same
            pic_path = './static/images/defaultProfilePic.jpg'

        # Below is checking validity of sign up forms

        user = User.query.filter_by(email=email).first()
        user_username = User.query.filter_by(username=username).first()
        
        
        if user:
            flash('Email already exists', category='error')
        elif user_username:
            flash('Username already exists', category='error')    
        elif len(email) < 4 or len(email) > 150:
            flash('Email must be between 4 and 150 characters long', category='error')
        elif len(username) < 2 or len(username) > 15:
            flash('Username must be between 2 and 15 characters long', category='error')
        elif password1 != password2:
            flash('Passwords must match', category='error')
        elif not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{7,}$', password1):
            flash('Password must be at least 7 characters long and contain at least one letter, one number, and one special character', category='error')
        else:

          
        
            # adds a new user
            new_user = User(email=email, username=username, password=generate_password_hash(
                password1, method='sha256'), score=0, profile_picture=pic_path)
            db.session.add(new_user)
            db.session.commit()
            # below makes new user follow themselves
            new_user.followed.append(new_user)
            db.session.commit()
            # remembers the fact that this user is logged in
            login_user(new_user, remember=True)
            flash('Account Created', category='success')
            return redirect(url_for('auth.home'))

    return render_template("sign_up.html")
