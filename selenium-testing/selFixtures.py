import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pytest, os
from website import create_app, db
from website.models import User
from flask_login import login_user
from io import BytesIO
from PIL import Image


# other imports...

@pytest.fixture(scope="session")
def app():
    app = create_app(f'sqlite://')
    app.testing = True
    with app.app_context():
        db.create_all()
    
    yield app
    
@pytest.fixture(scope="session")
def client(app):
    return app.test_client()

@pytest.fixture
def authenticated_user(client):
    
    file = BytesIO()
    image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    data = {
        "email": "auth@test", 
        "username": "MrAuth", 
        "password1": "authPass1!", 
        "password2": "authPass1!",
        "profile_picture": (file, "test.png")
    }

    with client:
        client.post("/sign-up", data=data, follow_redirects=True)
        yield client
    
    with client:
        client.get("/logout")

@pytest.fixture
def driver():
    driver = webdriver.Chrome(service=Service('selenium-testing\chromedriver.exe'))
    driver.implicitly_wait(10)  # seconds
    yield driver
    driver.quit()
