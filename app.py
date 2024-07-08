from flask import Flask
from flask_cors import CORS
from database import db, init_db
from routes import init_routes
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///debate_website.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Enable CORS
CORS(app)

with app.app_context():
    init_db()

init_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
