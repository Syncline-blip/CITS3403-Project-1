from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/')
def intro():
    return render_template("intro.html", user=current_user)


@views.route('/chat_room_1')
@login_required  # makes this page accessible only if user is logged in
def chat_room_1():
    return render_template("chat_room_1.html", user=current_user)


@views.route('/chat_room_2')
@login_required  # makes this page accessible only if user is logged in
def chat_room_2():
    return render_template("chat_room_2.html", user=current_user)


@views.route('/chat_room_3')
@login_required  # makes this page accessible only if user is logged in
def chat_room_3():
    return render_template("chat_room_3.html", user=current_user)

@views.route('/about_us')
@login_required  # makes this page accessible only if user is logged in
def about_us():
    return render_template("about_us.html", user=current_user)

@views.route('/user_terms')
@login_required  # makes this page accessible only if user is logged in
def user_terms():
    return render_template("user_terms.html", user=current_user)

@views.route('/privacy')
@login_required  # makes this page accessible only if user is logged in
def privacy():
    return render_template("privacy.html", user=current_user)


@views.route('/contact_us')
@login_required  # makes this page accessible only if user is logged in
def contact_us():
    return render_template("contact_us.html", user=current_user)
