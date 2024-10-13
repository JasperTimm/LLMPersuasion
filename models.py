import json
from database import db
from flask_login import UserMixin

all_debate_types = [
    'argument',
    'argumentllm',
    'simple',
    'stats',
    'personalized',
    'mixed'
]

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    total_debates = db.Column(db.Integer, nullable=False, default=0)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    finished = db.Column(db.Boolean, nullable=False, default=False)
    concluded = db.Column(db.Boolean, nullable=False, default=False)
    user_info = db.relationship('UserInfo', backref='user', uselist=False)
    quiz_completed = db.Column(db.Boolean, nullable=False, default=False)
    participant_id = db.Column(db.String(150), nullable=True)
    participant_service = db.Column(db.String(150), nullable=True)
    participant_status = db.Column(db.Text, nullable=True, default='{}')

    @property
    def participant_status_dict(self):
        if not self.participant_status:
            return {}
        return json.loads(self.participant_status)

    @participant_status_dict.setter
    def participant_status_dict(self, value):
        self.participant_status = json.dumps(value)

class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)    
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(50), nullable=True)
    profession = db.Column(db.String(150), nullable=True)
    education_level = db.Column(db.String(150), nullable=True)
    country_most_time = db.Column(db.String(150), nullable=True)
    extraverted_enthusiastic = db.Column(db.Integer)
    critical_quarrelsome = db.Column(db.Integer)
    dependable_self_disciplined = db.Column(db.Integer)
    anxious_easily_upset = db.Column(db.Integer)
    open_to_experiences_complex = db.Column(db.Integer)
    reserved_quiet = db.Column(db.Integer)
    sympathetic_warm = db.Column(db.Integer)
    disorganized_careless = db.Column(db.Integer)
    calm_emotionally_stable = db.Column(db.Integer)
    conventional_uncreative = db.Column(db.Integer)

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)

class CopyPasteEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10), nullable=False)
    data = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    current_page = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    debate_id = db.Column(db.String, db.ForeignKey('debate.id'), nullable=False)

class DebateLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    debate_id = db.Column(db.String, db.ForeignKey('debate.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    action = db.Column(db.String, nullable=False)

class DebateResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    debate_id = db.Column(db.String, db.ForeignKey('debate.id'), nullable=False)
    user_rating = db.Column(db.String, nullable=False)
    ai_rating = db.Column(db.String, nullable=False)
    time_spent = db.Column(db.Integer, nullable=False)  # Time spent in seconds
    feedback = db.Column(db.Text, nullable=False, default='{}')
    requires_review = db.Column(db.Boolean, default=False)
    review_reasons = db.Column(db.Text, nullable=True, default='[]')  # List of reasons for review as JSON string
    extended_reasons = db.Column(db.Text, nullable=True, default='[]')  # List of JSON objects for extended reasons

    @property
    def feedback_dict(self):
        return json.loads(self.feedback)

    @feedback_dict.setter
    def feedback_dict(self, value):
        self.feedback = json.dumps(value)

    @property
    def review_reasons_list(self):
        return json.loads(self.review_reasons)

    @review_reasons_list.setter
    def review_reasons_list(self, value):
        self.review_reasons = json.dumps(value)

    @property
    def extended_reasons_list(self):
        return json.loads(self.extended_reasons)

    @extended_reasons_list.setter
    def extended_reasons_list(self, value):
        self.extended_reasons = json.dumps(value)

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
    inactive_time = db.Column(db.Integer, nullable=False, default=0)

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
