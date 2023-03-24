from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
def intro():
    return render_template("intro.html", user=current_user)

@views.route('/home')
@login_required #makes this page accessible only if user is logged in
def home():
    return render_template("home.html", user=current_user)