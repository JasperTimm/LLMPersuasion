import json
from database import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    total_debates = db.Column(db.Integer, nullable=False, default=0)

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)

class Debate(db.Model):
    id = db.Column(db.String, primary_key=True)
    state = db.Column(db.String, nullable=False, default='intro')
    user_side = db.Column(db.String, nullable=False, default='')
    ai_side = db.Column(db.String, nullable=False, default='')
    initial_opinion = db.Column(db.Text, nullable=True)
    initial_likert_score = db.Column(db.Integer, nullable=True)
    user_responses = db.Column(db.Text, nullable=False, default='{}')
    llm_responses = db.Column(db.Text, nullable=False, default='{}')
    final_opinion = db.Column(db.Text, nullable=True)
    final_likert_score = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    debate_count = db.Column(db.Integer, nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    llm_model_type = db.Column(db.String, nullable=False, default='')
    llm_debate_type = db.Column(db.String, nullable=False, default='')
    chat_history = db.Column(db.Text, nullable=False, default='{}')

    @property
    def user_responses_dict(self):
        return json.loads(self.user_responses)

    @user_responses_dict.setter
    def user_responses_dict(self, value):
        self.user_responses = json.dumps(value)

    @property
    def llm_responses_dict(self):
        return json.loads(self.llm_responses)

    @llm_responses_dict.setter
    def llm_responses_dict(self, value):
        self.llm_responses = json.dumps(value)

    @property
    def chat_history_dict(self):
        return json.loads(self.chat_history)

    @chat_history_dict.setter
    def chat_history_dict(self, value):
        self.chat_history = json.dumps(value)