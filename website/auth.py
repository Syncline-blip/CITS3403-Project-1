import select
import os
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, session
from sqlalchemy import not_
from .models import User, followers
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import uuid as uuid
from werkzeug.utils import secure_filename
import random
from string import ascii_uppercase
from .constants import rooms
from . import socketio


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

auth = Blueprint('auth', __name__)

def genCode(Length):
    while True:
        code = ''
        for _ in range(Length):
            code += random.choice(ascii_uppercase)
        
        if code not in rooms:
            break
    
    return code

@auth.route("/home", methods=["POST", "GET"])
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
            return render_template("home.html", error="Please enter a room code.", code=code, user=current_user)
        
       
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
            return render_template("home.html", error="Room '" +code+"' does not exist", user=current_user)

        #temporary data
        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("home.html",user=current_user)

'''@auth.route('/home')
@login_required  # makes this page accessible only if user is logged in
def home():
    return render_template("home.html", user=current_user)'''

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

@auth.route('/add_friend',methods=['GET','POST'])
@login_required
def add_friend():
    user = current_user
    number = int(request.form.get('friend_id'))
    friend = User.query.filter_by(id=number).first()
    user.followed.append(friend)
    db.session.commit()
    return redirect(url_for('auth.friends_list'))

@auth.route('/remove_friend',methods=['GET','POST'])
@login_required
def remove_friend():
    user = current_user
    number = int(request.form.get('friend_id'))
    friend = User.query.filter_by(id=number).first()
    user.followed.remove(friend)
    db.session.commit()
    return redirect(url_for('auth.friends_list'))



@auth.route('/scoreboard')
@login_required
def scoreboard():
    num_users = db.session.query(User).count()
    top_three_scores = None
    
    if num_users > 3:
        #Gets the top three scores but then changes the order from 1,2,3 to 2,1,3
        top_three_scores = User.query.order_by(User.score.desc()).limit(3).all()
        top_three_scores[1], top_three_scores[0], top_three_scores[2] = top_three_scores[0], top_three_scores[1], top_three_scores[2]
        #Gets all the other scores in descending order
        other_scores = User.query.order_by(User.score.desc()).offset(3).all()
    else:
        #If the User count <= 3 we display all users in the table
        other_scores = User.query.order_by(User.score.desc()).all()
    return render_template("scoreboard.html", user=current_user, top_three_scores=top_three_scores, other_scores=other_scores, num_users=num_users)

@auth.route('/friends_list')
@login_required
def friends_list():
    friends_list = current_user.followed.order_by(User.first_name).filter(User.id!=current_user.id)
    not_friends_list = User.query.filter(not_(User.id.in_([user.id for user in current_user.followed]))).all()
    return render_template("friends_list.html", user=current_user, friends_list=friends_list, not_friends_list=not_friends_list)

#checks if the filenames extension is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth.route('/account', methods=['GET', 'POST'])
@login_required  # makes this page accessible only if user is logged in
def account():
    if request.method == 'POST':
        user = current_user

        new_email = request.form.get('email')
        new_first_name = request.form.get('firstName')
        new_password1 = request.form.get('password1')
        new_password2 = request.form.get('password2')

        
        
        if request.files.get('pic').filename == '':
            pic_path = user.image_file
        else:
            img = request.files.get('pic')
            if img and allowed_file(img.filename):
                #Get image name
                pic_filename = secure_filename(img.filename)
                #Set unique image name
                pic_name = str(uuid.uuid1()) + "_" + pic_filename
                #Save image
                img.save(os.path.join(current_app.root_path, 'static/images/profile_pictures', pic_name))
                #get image path
                pic_path = './static/images/profile_pictures/' + pic_name
            else:
                flash('Uploaded image must be a png, jpg or jpeg', category='error')
                return render_template("account.html", user=current_user)
        

        #check if email changing to already exists
        other_user = User.query.filter_by(email=new_email).first()

        '''
        TODO
        #if the email matches another user who is NOT the current user, email changing fails
        if other_user and other_user.id != user.id:
            flash('Email already exists', category='error')
        elif len(new_email) < 4:
            flash('Email must be greater then 3 characters', category='error')
        elif len(new_first_name) < 2:
            flash('First name must be greater then 1 characters', category='error')
        elif new_password1 != new_password2:
            flash('Passwords don\'t match', category='error')
        elif new_password1 == "" and new_password2 == "":
            user.email = new_email
            user.first_name = new_first_name
            db.session.commit()
            flash('Account updated', category='success')
            return redirect(url_for('auth.home'))
        elif len(new_password1) < 7:
            flash('Password must be greater then 7 characters', category='error')
        else:
        '''
        user.email = new_email
        user.first_name = new_first_name
        user.password = generate_password_hash(new_password1, method='sha256')
        user.image_file = pic_path
        db.session.commit()
        flash('Account updated', category='success')
        return redirect(url_for('auth.home'))
        

    return render_template("account.html", user=current_user)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')


    
        if request.files.get('pic').filename == '':
            pic_path = './static/images/defaultProfilePic.jpg'
        else:
            img = request.files.get('pic')
            if img and allowed_file(img.filename):
                #Get image name
                pic_filename = secure_filename(img.filename)
                #Set unique image name
                pic_name = str(uuid.uuid1()) + "_" + pic_filename
                #Save image
                img.save(os.path.join(current_app.root_path, 'static/images/profile_pictures', pic_name))
                #get image path
                pic_path = './static/images/profile_pictures/' + pic_name
            else:
                flash('Uploaded image must be a png, jpg or jpeg', category='error')
                return render_template("sign_up.html", user=current_user)


        # Below is checking validity of sign up forms

        user = User.query.filter_by(email=email).first()
        """ 
        TODO
        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('Email must be greater then 3 characters', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater then 1 characters', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash('Password must be greater then 7 characters', category='error')
        else:
        """
        # adds a new user
        new_user = User(email=email, first_name=first_name, password=generate_password_hash(
            password1, method='sha256'), score=0, image_file=pic_path)
        db.session.add(new_user)
        db.session.commit()
        #below makes new user follow themselves
        new_user.followed.append(new_user)
        db.session.commit()
        # remembers the fact that this user is logged in
        login_user(new_user, remember=True)
        flash('Account created', category='success')
        return redirect(url_for('auth.home'))

    return render_template("sign_up.html", user=current_user)
