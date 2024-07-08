import json
from database import db

class Debate(db.Model):
    id = db.Column(db.String, primary_key=True)
    topic = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False, default='intro')
    user_side = db.Column(db.String, nullable=False)
    ai_side = db.Column(db.String, nullable=False)    
    user_responses = db.Column(db.Text, nullable=False, default='[]')
    llm_responses = db.Column(db.Text, nullable=False, default='[]')

    @property
    def user_responses_list(self):
        return json.loads(self.user_responses)

    @user_responses_list.setter
    def user_responses_list(self, value):
        self.user_responses = json.dumps(value)

    @property
    def llm_responses_list(self):
        return json.loads(self.llm_responses)

    @llm_responses_list.setter
    def llm_responses_list(self, value):
        self.llm_responses = json.dumps(value)
