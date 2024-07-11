import json
from database import db

class Debate(db.Model):
    id = db.Column(db.String, primary_key=True)
    topic = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False, default='intro')
    user_side = db.Column(db.String, nullable=False, default='')
    ai_side = db.Column(db.String, nullable=False, default='')
    user_initial_opinion = db.Column(db.Text, nullable=True)
    user_likert_score = db.Column(db.Integer, nullable=True)
    user_responses = db.Column(db.Text, nullable=False, default='{}')
    llm_responses = db.Column(db.Text, nullable=False, default='{}')

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
