from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
import os
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

def add_admin_user():
    admin_pwd = os.environ.get('ADMIN_PASSWORD', 'password')
    hashed_password = generate_password_hash(admin_pwd, method='pbkdf2:sha256')
    user = User(username='admin', password=hashed_password, admin=True)
    db.session.add(user)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        init_db()
        add_admin_user()
        populate_topics()    