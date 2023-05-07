from website.models import User, db
from flask_login import current_user, login_user
import os
from io import BytesIO
from PIL import Image

def test_authenticated_user(client, authenticated_user):
    # Ensure the user is logged in
    response = authenticated_user.get("/home", follow_redirects=True)
    assert response.status_code == 200
    assert User.query.count() == 1


    # Log the user out
    response = authenticated_user.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"<title>Login</title>" in response.data

def test_intro(client):
    response = client.get("/")
    assert b"<title>Intro</title>" in response.data

def test_sign_up(client, app):
    #create a new user
    file = BytesIO()
    image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    data = {
        "email": "test@test", 
        "first_name": "MrTest", 
        "password1": "testPass", 
        "password2": "testPass",
        "pic": (file, "test.png")
    }
    #sign up with the above data
    response = client.post("/sign-up", data=data, follow_redirects=True)
    #check if the new user is redirected to the home page and has thier details stored in the db
    assert b"<title>Home</title>" in response.data
    assert b"Account created" in response.data
    assert User.query.count() == 1
    assert User.query.first().email == "test@test"
    
def test_login(client, authenticated_user):
    #check if login page is accessible
    response = client.get("/login")
    assert response.status_code == 200
    assert b"<title>Login</title>" in response.data

    #login using the authenticated user details
    data = {"email": "auth@test", "password": 'authPass'}
    #check if correctly redirected to the home page
    response = client.post("/login", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"<title>Home</title>" in response.data
    assert b'Logged in successfully!' in response.data
    
    #try to login with invalid email
    data = {'email': "not@real", 'password': 'authPass'}
    response = client.post('/login', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Email does not exist' in response.data
    
    #try to login with valid email but incorrect password
    data = {'email': "auth@test", 'password': 'wrongpassword'}
    response = client.post('/login', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Incorrect password, try again' in response.data

def test_logout(client, authenticated_user):
    #check the user is logged in on the home page
    response = client.get("/home", follow_redirects=True)
    assert b"<title>Home</title>" in response.data
    
    #check logout works and sends the user to the login page
    response = client.get('/logout', follow_redirects=True)
    assert b"<title>Login</title>" in response.data

    #check that the user cant access a page that requires the user to be logged in
    response = client.get('/account', follow_redirects=True)
    assert b"<title>Intro</title>" in response.data
    assert b'Please log in to access this page' in response.data
    
def test_home(client, authenticated_user):
    #test access to the home page
    response = client.get("/home", follow_redirects=True)
    assert b"<title>Home</title>" in response.data
    assert User.query.count() == 1
    assert User.query.first().email == "auth@test"

def test_account(client, authenticated_user):
    #test access to the home page
    response = client.get("/account", follow_redirects=True)
    assert b"<title>Account</title>" in response.data

def test_about_us(client, authenticated_user):
    #test access to the about us page
    response = client.get("/about_us", follow_redirects=True)
    assert b"<title>About Us</title>" in response.data

def test_user_terms(client, authenticated_user):
    #test access to the user terms page
    response = client.get("/user_terms", follow_redirects=True)
    assert b"<title>User Terms</title>" in response.data

def test_privacy(client, authenticated_user):
    #test access to the privacy page
    response = client.get("/privacy", follow_redirects=True)
    assert b"<title>Privacy</title>" in response.data