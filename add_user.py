import sys
from werkzeug.security import generate_password_hash
from database import db
from models import User
from app import app

def add_user(username, password):
    with app.app_context():
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        print(f"User {username} added successfully.")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python add_user.py <username> <password>")
    else:
        username = sys.argv[1]
        password = sys.argv[2]
        add_user(username, password)