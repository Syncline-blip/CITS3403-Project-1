import os
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, session
from sqlalchemy import not_, or_
from .models import User, followers, Messages, Room
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import uuid as uuid
from werkzeug.utils import secure_filename
import random
from string import ascii_uppercase



ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

auth = Blueprint('auth', __name__)


def genCode(Length):
    while True:
        code = ''
        for _ in range(Length):
            code += random.choice(ascii_uppercase)

        room = Room.query.filter_by(room_name=code).first()
        if room is None:
            break

    return code


@auth.route("/home", methods=["POST", "GET"])
@login_required  # makes this page accessible only if user is logged in
def home():

    #Code for the favourite and members List
    favourite_list = current_user.followed.order_by(
        User.username).filter(User.id != current_user.id)
    not_favourite_list = User.query.filter(
        not_(User.id.in_([user.id for user in current_user.followed]))).all()
    
    #Code for the leaderboard
    num_users = db.session.query(User).count()
    top_three_scores = None
    if num_users > 3:
        # Gets the top three scores but then changes the order from 1,2,3 to 2,1,3
        top_three_scores = User.query.order_by(
            User.score.desc()).limit(3).all()
        top_three_scores[1], top_three_scores[0], top_three_scores[2] = top_three_scores[0], top_three_scores[1], top_three_scores[2]
        # Gets all the other scores in descending order
        other_scores = User.query.order_by(User.score.desc()).offset(3).all()
    else:
        # If the User count <= 3 we display all users in the table
        other_scores = User.query.order_by(User.score.desc()).all()

    session.clear()
    if request.method == "POST":
        username = current_user.username
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)
        globalChat = request.form.get("globalChat", False)
        anonChat = request.form.get("anonChat", False)
        supportChat = request.form.get("supportChat", False)

        # If We allow custom usernames we need this check.
        # if not name:
        #    return render_template("home.html", error="Please enter a name.", code=code, name=name)

        if join != False and not code:
            print("I AM HEREEEE")
            return render_template("home.html", error="Please enter a room code.", code=code, user=current_user)

        if globalChat != False:
            session["room"] = "GLOB"
            session["username"] = username
            return redirect(url_for("auth.room"))
        elif anonChat != False:
            session["room"] = "ANON"
            session["username"] = "Anonymous"
            return redirect(url_for("auth.room"))
        elif supportChat != False:
            session["room"] = "SUPP"
            session["username"] = username
            return redirect(url_for("auth.room"))

        new_room_name = code
        room = Room.query.filter_by(room_name=new_room_name).first()
        if create != False:
            new_room_name = genCode(4)
            new_room = Room(room_name=new_room_name, description=f'Custom Room {new_room_name}')
            db.session.add(new_room)
            db.session.commit()
        elif room is None:
            print("I am here so it's interesting...")
            return render_template("home.html", error="Room '" + code+"' does not exist", user=current_user)

        # temporary data
        session["room"] = new_room_name
        session["username"] = username
        return redirect(url_for("auth.room"))

    return render_template("home.html", user=current_user,favourite_list=favourite_list, not_favourite_list=not_favourite_list,top_three_scores=top_three_scores, other_scores=other_scores, num_users=num_users)


@auth.route("/room")
@login_required  # makes this page accessible only if user is logged in
def room():
    current_room_name = session.get("room")
    if current_room_name is None or session.get("username") is None:
        return redirect(url_for("auth.home"))
    
    room = Room.query.filter_by(room_name=current_room_name).first()
    if room is None:
        return redirect(url_for("auth.home"))
    
    # Load messages associated with this room
    messages = db.session.query(Messages, User.username, User.profile_picture)\
                    .join(User, User.id == Messages.user_id)\
                    .filter(Messages.room_id == room.id)\
                    .all()

    return render_template("room.html", room=room, messages=messages, user=current_user)

@auth.route('/search_messages')
def search_messages():
    query = request.args.get('query')
    room_id = request.args.get('room_id')
    if not query:
        return ''

    # Check if the query starts with './from'
    search_by_user = query.startswith('./from')

    if search_by_user:
        # Remove './from' from the query and strip any leading/trailing spaces
        query = query.replace('./from', '').strip()

    messages = db.session.query(Messages, User.username, User.profile_picture)\
                .join(User, Messages.user_id == User.id)\
                .filter(Messages.room_id == room_id)

    if search_by_user:
        # Filter by username
        messages = messages.filter(User.username.like(f'%{query}%'))
    else:
        # Filter by message content
        messages = messages.filter(Messages.data.like(f'%{query}%'))

    messages = messages.all()

    return render_template('messages.html', messages=messages)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # filter all of the users that have this email and retun the first result (should only be 1)
        user = User.query.filter_by(email=email).first()
        if user:
            # if passwords are the same
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                # remembers the fact that this user is logged in
                login_user(user, remember=True)
                return redirect(url_for('auth.home'))
            else:
                # if password arent the same
                flash('Incorrect password, try again.', category='error')
        else:
            # if email doesnt exist
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required  # makes this page accessible only if user is logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


# increases users score by 1
@auth.route('/add', methods=['POST'])
def add():
    user = current_user
    user.score = user.score + 1
    db.session.commit()
    return redirect(url_for('auth.home'))


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

        if request.files.get('pic').filename == '':
            pic_path = user.profile_picture
        else:
            img = request.files.get('pic')
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
                return render_template("account.html", user=current_user)

        # check if email changing to already exists
        other_user = User.query.filter_by(email=new_email).first()
        other_user_username = User.query.filter_by(username=new_username).first()

        '''
        TODO
        #if the email matches another user who is NOT the current user, email changing fails
        if other_user and other_user.id != user.id:
            flash('Email already exists', category='error')
        elif other_user_username and other_user.id != user.id:
            flash('Username already exists', category='error')
        elif len(new_email) < 4:
            flash('Email must be greater then 3 characters', category='error')
        elif len(new_username) < 2:
            flash('Username must be greater then 1 characters', category='error')
        elif new_password1 != new_password2:
            flash('Passwords don\'t match', category='error')
        elif new_password1 == "" and new_password2 == "":
            user.email = new_email
            user.username = new_username
            db.session.commit()
            flash('Account updated', category='success')
            return redirect(url_for('auth.home'))
        elif len(new_password1) < 7:
            flash('Password must be greater then 7 characters', category='error')
        else:
        '''
        user.email = new_email
        user.username = new_username
        user.password = generate_password_hash(new_password1, method='sha256')
        user.profile_picture = pic_path
        db.session.commit()
        flash('Account updated', category='success')
        return redirect(url_for('auth.home'))

    return render_template("account.html", user=current_user)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if request.files.get('pic').filename == '':
            pic_path = './static/images/defaultProfilePic.jpg'
        else:
            img = request.files.get('pic')
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
                return render_template("sign_up.html", user=current_user)

        # Below is checking validity of sign up forms

        user = User.query.filter_by(email=email).first()
        user_username = User.query.filter_by(username=username).first()
        """ 
        TODO
        if user:
            flash('Email already exists', category='error')
        elif user_username:
            flash('Username already exists', category='error')    
        elif len(email) < 4:
            flash('Email must be greater then 3 characters', category='error')
        elif len(username) < 2:
            flash('Username must be greater then 1 characters', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash('Password must be greater then 7 characters', category='error')
        else:
        """
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
        flash('Account created', category='success')
        return redirect(url_for('auth.home'))

    return render_template("sign_up.html", user=current_user)
