import pytest, os
from website import create_app, db
from website.models import User
from flask_login import login_user
from io import BytesIO
from PIL import Image


DB_NAME = "Testdatabase.db"

@pytest.fixture()
def app():
    app = create_app(f'sqlite:///{DB_NAME}')
    app.testing = True
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

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
        "first_name": "MrAuth", 
        "password1": "authPass", 
        "password2": "authPass",
        "pic": (file, "test.png")
    }

    with client:
        client.post("/sign-up", data=data, follow_redirects=True)
        yield client
    
    

    with client:
        client.get("/logout")

    

    #user = User(data)
    #db.session.add(user)
    #db.session.commit()

    #with app.app_context():
        #db.session.delete(user)
        #db.session.commit()