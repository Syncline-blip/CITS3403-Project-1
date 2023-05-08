from website.models import User, db
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
    #test access to the sign up page
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
        assert User.query.first().email == "test@pass"
        assert User.query.first().username == "MrPass"
        assert User.query.first().profile_picture == "./static/images/defaultProfilePic.jpg"

    #signing up with correct values and uploading a custom image 
    file1 = BytesIO()
    image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
    image.save(file1, 'png')
    file1.name = 'test.png'
    file1.seek(0)
    data = {
        "email": "test@pic", 
        "username": "MrPic", 
        "password1": "testPass", 
        "password2": "testPass",
        "profile_picture": (file1, "test.png")
    }
    response = client.post("/sign-up", data=data, follow_redirects=True)
    with app.app_context():
        #check if the new user is redirected to the home page and has their details stored in the db
        assert response.status_code == 200
        assert b"<title>Home</title>" in response.data
        assert b"Account Created" in response.data
        user = User.query.filter_by(email='test@pic').first()
        assert user.username == "MrPic"
        assert "test.png" in user.profile_picture 

    #tring to signup with already taken email
    data = {
        "email": "test@pass", 
        "username": "MrFail", 
        "password1": "testPass", 
        "password2": "testPass",
    }
    response = client.post("/sign-up", data=data, follow_redirects=True)
    with app.app_context():
        #check if the new user is redirected to the home page and has their details stored in the db
        assert response.status_code == 200
        assert b"<title>Sign Up</title>" in response.data   
        assert b"Email already exists" in response.data
        
    #tring to signup with already taken username
    data = {
        "email": "test@fail", 
        "username": "MrPass", 
        "password1": "testPass", 
        "password2": "testPass",
    }
    response = client.post("/sign-up", data=data, follow_redirects=True)
    with app.app_context():
        #check if the new user is redirected to the home page and has their details stored in the db
        assert response.status_code == 200
        assert b"<title>Sign Up</title>" in response.data   
        assert b"Username already exists" in response.data

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

    #trying to signup with invalid username
    data = {
        "email": "test@test", 
        "username": "f", 
        "password1": "testPass", 
        "password2": "testPass",
    }
    response = client.post("/sign-up", data=data, follow_redirects=True)
    with app.app_context():
        assert response.status_code == 200
        assert b"<title>Sign Up</title>" in response.data   
        assert b"Username must be greater then 1 character" in response.data
        assert not User.query.filter_by(email="test@test").first()

    #trying to signup with invalid password
    data = {
        "email": "test@test", 
        "username": "GoodName", 
        "password1": "small", 
        "password2": "small",
    }
    response = client.post("/sign-up", data=data, follow_redirects=True)
    with app.app_context():
        assert response.status_code == 200
        assert b"<title>Sign Up</title>" in response.data   
        assert b"Password must be greater then 7 characters" in response.data
        assert not User.query.filter_by(email="test@test").first()

    #trying to signup with non matching passwords
    data = {
        "email": "test@test", 
        "username": "GoodName", 
        "password1": "testPass", 
        "password2": "testPass2",
    }
    response = client.post("/sign-up", data=data, follow_redirects=True)
    with app.app_context():
        assert response.status_code == 200
        assert b"<title>Sign Up</title>" in response.data   
        assert b"Passwords must match" in response.data
        assert not User.query.filter_by(email="test@test").first()

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
    assert response.status_code == 200
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
    assert response.status_code == 200
    assert b"<title>Home</title>" in response.data
    assert User.query.first().email == "auth@test"
    assert User.query.first().username == "MrAuth"
    assert b'Account Updated' in response.data

    #test changing the email
    data["email"] = "authNew@test"
    response = client.post("/account", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"<title>Home</title>" in response.data
    assert User.query.first().email == "authNew@test"
    assert User.query.first().username == "MrAuth"
    assert b'Account Updated' in response.data

    #test changing the username
    data["username"] = "MrNew"
    response = client.post("/account", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"<title>Home</title>" in response.data
    assert User.query.first().email == "authNew@test"
    assert User.query.first().username == "MrNew"
    assert b'Account Updated' in response.data

    #test changing password
    data["password1"] = "wEbDevER"
    data["password2"] = "wEbDevER"
    response = client.post("/account", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"<title>Home</title>" in response.data
    assert User.query.first().email == "authNew@test"
    assert User.query.first().username == "MrNew"   
    assert b'Account Updated' in response.data  
    # Log out the user
    client.get("/logout", follow_redirects=True)
    # Log in with new credentials
    response = client.post("/login", data={"email": "authNew@test", "password": "wEbDevER"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"<title>Home</title>" in response.data
    assert b"Logged in successfully!" in response.data

def test_account_fails(client, authenticated_user):
    #tests incorrect update methods

    #test access to the sign up page
    response = client.get("/sign-up", follow_redirects=True)
    assert response.status_code == 200
    assert b"<title>Sign Up</title>" in response.data

    #create a second user
    assert User.query.count() == 1
    data = {
        "email": "test@pass", 
        "username": "MrPass", 
        "password1": "testPass", 
        "password2": "testPass",
    }
    response = client.post("/sign-up", data=data, follow_redirects=True)
    #check if the new user is redirected to the home page and has their details stored in the db
    assert response.status_code == 200
    assert b"<title>Home</title>" in response.data
    assert b"Account Created" in response.data
    user = User.query.filter_by(email='test@pass').first()
    assert user.username == "MrPass"
    assert User.query.count() == 2
    
    #test access to the account page
    response = client.get("/account", follow_redirects=True)
    assert response.status_code == 200
    assert b"<title>Account</title>" in response.data   
    assert user.username == "MrPass"
    
    #tring to change to already taken email
    data = {
        "email": "auth@test", 
        "username": "MrPass", 
        "password1": "", 
        "password2": "",
    }
    response = client.post("/account", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"<title>Account</title>" in response.data   
    assert b"Email already exists" in response.data

    #tring to change to already taken username
    data = {
        "email": "test@path", 
        "username": "MrAuth", 
        "password1": "", 
        "password2": "",
    }
    response = client.post("/account", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"<title>Account</title>" in response.data   
    assert b"Username already exists" in response.data

    #trying to change to invalid email
    data = {
        "email": "t@t", 
        "username": "MrPass", 
        "password1": "", 
        "password2": "",
    }
    response = client.post("/account", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"<title>Account</title>" in response.data   
    assert b"Email must be greater then 3 characters" in response.data
    assert not User.query.filter_by(email="t@t").first()

    #trying to change to invalid username
    data = {
        "email": "test@path", 
        "username": "f", 
        "password1": "", 
        "password2": "",
    }
    response = client.post("/account", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"<title>Account</title>" in response.data   
    assert b"Username must be greater then 1 character" in response.data
    assert not User.query.filter_by(username="f").first()

    #trying to change to invalid password
    data = {
        "email": "test@path", 
        "username": "MrPass", 
        "password1": "small", 
        "password2": "small",
    }
    response = client.post("/account", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"<title>Account</title>" in response.data   
    assert b"Password must be greater then 7 characters" in response.data
    
    #trying to change to non matching password
    data = {
        "email": "test@path", 
        "username": "MrPass", 
        "password1": "testPass", 
        "password2": "testPass2",
    }
    response = client.post("/account", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"<title>Account</title>" in response.data   
    assert b"Passwords must match" in response.data

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