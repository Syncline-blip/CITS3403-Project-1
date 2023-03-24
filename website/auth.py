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

        user = User.query.filter_by(email=email).first() #filter all of the users that have this email and retun the first result (should only be 1)
        if user:
            if check_password_hash(user.password, password): #if passwords are the same
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True) #remembers the fact that this user is logged in
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error') #if password arent the same
        else:
            flash('Email does not exist.', category='error') #if email doesnt exist

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required #makes this page accessible only if user is logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #Below is checking validity of sign up forms

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
            flash('Password don\'t match', category='error')
        elif len(password1) < 7:
            flash('Password must be greater then 7 characters', category='error')
        else:
        """
        #adds a new user
        new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True) #remembers the fact that this user is logged in
        flash('Account created', category='success')
        return redirect(url_for('views.home'))


    return render_template("sign_up.html", user=current_user)