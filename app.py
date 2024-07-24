from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
import os

from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from database import db, init_db
from models import User
from routes import init_routes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///debate_website.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Enable CORS
CORS(app, supports_credentials=True)

# Set the secret key from an environment variable
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')

# Configure session cookie settings
app.config.update(
    SESSION_COOKIE_SAMESITE='None',
    SESSION_COOKIE_SECURE=True
)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    init_db()

init_routes(app)

if __name__ == '__main__':
    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'production':
        # In prod we have SSL termination from the web server
        app.run(debug=False)
    else:
        app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))
