import pytest, os
from website import create_app, db
from website.models import User
from flask_login import login_user
from io import BytesIO
from PIL import Image


DB_NAME = "Testdatabase.db"

@pytest.fixture()
def app():
    app = create_app(f'sqlite://')
    app.testing = True
    with app.app_context():
        db.create_all()
    
    yield app
        

@pytest.fixture()
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
        "password1": "authPass", 
        "password2": "authPass",
        "profile_picture": (file, "test.png")
    }

    with client:
        client.post("/sign-up", data=data, follow_redirects=True)
        yield client
    
    with client:
        client.get("/logout")
