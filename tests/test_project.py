from website.models import User, db
from flask_login import current_user, login_user
import os
from io import BytesIO
from PIL import Image

def test_authenticated_user(client, authenticated_user):
    # Ensure the user is logged in
    response = authenticated_user.get("/home", follow_redirects=True)
    assert response.status_code == 200
    assert User.query.first().email == "auth@test"
    assert User.query.first().username == "MrAuth"
    assert User.query.count() == 1

    # Log the user out
    response = authenticated_user.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"<title>Login</title>" in response.data
    assert b'Logged out successfully!' in response.data

def test_intro(client):
    response = client.get("/")
    assert b"<title>Intro</title>" in response.data









def test_sign_up(client, app):
    #test access to the account page
    response = client.get("/sign-up", follow_redirects=True)
    assert response.status_code == 200
    assert b"<title>Sign Up</title>" in response.data

    #test several ways of signing up
    
    #signing up with correct values and not uploading an image so the user gets the defaultProfilePic.jpg
    data = {
        "email": "test@pass", 
        "username": "MrPass", 
        "password1": "testPass", 
        "password2": "testPass",
    }
    response = client.post("/sign-up", data=data, follow_redirects=True)
    with app.app_context():
        #check if the new user is redirected to the home page and has their details stored in the db
        assert response.status_code == 200
        assert b"<title>Home</title>" in response.data
        assert b"Account Created" in response.data
        assert User.query.count() == 1
        assert User.query.first().email == "test@pass"
        assert User.query.first().username == "MrPass"
        assert User.query.first().profile_picture == "./static/images/defaultProfilePic.jpg"

    #trying to signup with invalid email
    data = {
        "email": "t@t", 
        "username": "MrTest", 
        "password1": "testPass", 
        "password2": "testPass",
    }
    response = client.post("/sign-up", data=data, follow_redirects=True)
    with app.app_context():
        assert response.status_code == 200
        assert b"<title>Sign Up</title>" in response.data   
        assert b"Email must be greater then 3 characters" in response.data
        assert not User.query.filter_by(email="t@t").first()



    '''file = BytesIO()
    image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    data = {
        "email": "test@test", 
        "username": "MrTest", 
        "password1": "testPass", 
        "password2": "testPass",
        "profile_picture": (file, "test.png")
    }'''





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
    assert User.query.first().email == "auth@test"
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
    assert b'Logged out successfully!' in response.data

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
    #test access to the account page
    response = client.get("/account", follow_redirects=True)
    assert User.query.first().email == "auth@test"
    assert User.query.first().username == "MrAuth"
    assert b"<title>Account</title>" in response.data
    
    #test several ways of altering the users details in the account page
   
    #test where nothing is changed
    #data is below as Account.html defaults to having the email and username input box prepopulated with the current email and username
    data = {
        "email": "auth@test", 
        "username": "MrAuth", 
        "password1": "", 
        "password2": "",
    }
    response = client.post("/account", data=data, follow_redirects=True)
    assert b"<title>Home</title>" in response.data
    assert User.query.first().email == "auth@test"
    assert User.query.first().username == "MrAuth"
    assert b'Account Updated' in response.data

    #test changing the email
    data["email"] = "authNew@test"
    response = client.post("/account", data=data, follow_redirects=True)
    assert b"<title>Home</title>" in response.data
    assert User.query.first().email == "authNew@test"
    assert User.query.first().username == "MrAuth"
    assert b'Account Updated' in response.data

    '''
    file = BytesIO()
    image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    data = {
        "email": "auth@test", 
        "username": "MrAuth", 
        "password1": "authPass", 
        "password2": "authPass",
        "profile_picture": (file, "test.png")
    }'''

    


    





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