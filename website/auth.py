from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


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
                return redirect(url_for('views.home'))
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
    return redirect(url_for('views.home'))


@auth.route('/scoreboard')
@login_required
def scoreboard():
    scores = User.query.order_by(User.score.desc()).all()
    return render_template("scoreboard.html", user=current_user, scores=scores)

@auth.route('/friends_list')
@login_required
def friends_list():
    friends_list = User.query.order_by(User.first_name)
    return render_template("friends_list.html", user=current_user, friends_list=friends_list)

@auth.route('/not_friends_list')
@login_required
def not_friends_list():
    not_friends_list = User.query.order_by(User.first_name)
    return render_template("not_friends_list.html", user=current_user, not_friends_list=not_friends_list)


@auth.route('/account', methods=['GET', 'POST'])
@login_required  # makes this page accessible only if user is logged in
def account():
    if request.method == 'POST':
        user = current_user

        new_email = request.form.get('email')
        new_first_name = request.form.get('firstName')
        new_password1 = request.form.get('password1')
        new_password2 = request.form.get('password2')


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
            return redirect(url_for('views.home'))
        elif len(new_password1) < 7:
            flash('Password must be greater then 7 characters', category='error')
        else:
        '''
        user.email = new_email
        user.first_name = new_first_name
        user.password = generate_password_hash(new_password1, method='sha256')
        db.session.commit()
        flash('Account updated', category='success')
        return redirect(url_for('views.home'))
        

    return render_template("account.html", user=current_user)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

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
            password1, method='sha256'), score=0)
        db.session.add(new_user)
        db.session.commit()
        # remembers the fact that this user is logged in
        login_user(new_user, remember=True)
        flash('Account created', category='success')
        return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
