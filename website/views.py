from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user

views = Blueprint('views', __name__)

#Injects the current user into the template context.
@views.app_context_processor
def inject_user():
    return dict(user=current_user)

#Define the route for the application root ('/') 
#If the current user is authenticated, they are redirected to the home page. If not, the intro page is displayed.
@views.route('/')
def intro():
    if current_user.is_authenticated:
        return redirect(url_for('auth.home'))
    else:
        return render_template("intro.html")

#Define the route for the about_us page. 
@views.route('/about_us')
def about_us():
    return render_template("about_us.html")

#Define the route for the privacy page.
@views.route('/privacy')
def privacy():
    return render_template("privacy.html")

#Define the route for the contact_us page.
@views.route('/contact_us')
def contact_us():
    return render_template("contact_us.html")