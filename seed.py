from models import Topic, User
from database import db, init_db
from topics import original_topics
from flask import Flask
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///debate_website.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def populate_topics():
    for description in original_topics:
        topic = Topic(description=description)
        db.session.add(topic)
    db.session.commit()

def add_users():
    # Add test user here for now
    hashed_password = generate_password_hash('password', method='pbkdf2:sha256')
    user = User(username='guest', password=hashed_password)
    db.session.add(user)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        init_db()
        add_users()
        populate_topics()    