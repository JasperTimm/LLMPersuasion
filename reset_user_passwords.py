import os
from werkzeug.security import generate_password_hash
from database import db
from models import User
from app import app

def reset_user_passwords():
    admin_pwd = os.environ.get('ADMIN_PASSWORD', 'password')
    hashed_password = generate_password_hash(admin_pwd, method='pbkdf2:sha256')

    with app.app_context():
        users = User.query.all()
        for user in users:
            user.password = hashed_password
        db.session.commit()
        print("All user passwords have been reset to the admin password.")

if __name__ == '__main__':
    reset_user_passwords()