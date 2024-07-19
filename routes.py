from flask import request, jsonify, redirect, url_for
import uuid
import random
from database import db
from models import Debate
from llm_handler import get_llm_response
from claims import original_claims
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User

def init_routes(app):
    @app.route('/login', methods=['POST'])
    def login():
        data = request.json
        username = data.get('username')
        password = data.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return jsonify({'message': 'Logged in successfully'}), 200
        return jsonify({'message': 'Invalid credentials'}), 401

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return jsonify({'message': 'Logged out successfully'}), 200

    @app.route('/protected')
    @login_required
    def protected():
        return jsonify({'message': f'Hello, {current_user.username}!'}), 200

    @app.route('/start_debate', methods=['POST'])
    @login_required
    def start_debate():
        debate_id = str(uuid.uuid4())
        topic = random.choice(original_claims)
        new_debate = Debate(id=debate_id, topic=topic, user_side='', ai_side='')
        db.session.add(new_debate)
        db.session.commit()
        
        response = {
            'debate_id': debate_id,
            'topic': topic
        }
        print(f"Started debate with ID: {debate_id} and topic: {topic}")
        return jsonify(response)

    @app.route('/update_position', methods=['POST'])
    @login_required
    def update_position():
        data = request.json
        debate_id = data.get('debate_id')
        user_initial_opinion = data.get('user_initial_opinion')
        likert_score = data.get('likert_score')

        debate = Debate.query.get(debate_id)
        if not debate:
            return jsonify({'error': 'Invalid debate ID'}), 400

        if likert_score in [1, 2, 3]:
            user_side = 'AGAINST'
        elif likert_score in [5, 6, 7]:
            user_side = 'FOR'
        else:
            user_side = random.choice(['FOR', 'AGAINST'])

        ai_side = 'AGAINST' if user_side == 'FOR' else 'FOR'
        debate.user_side = user_side
        debate.ai_side = ai_side
        debate.user_initial_opinion = user_initial_opinion
        debate.user_likert_score = likert_score

        db.session.commit()
        
        response = {
            'debate_id': debate_id,
            'user_side': user_side,
            'ai_side': ai_side
        }
        return jsonify(response)

    @app.route('/update_debate', methods=['POST'])
    @login_required
    def update_debate():
        data = request.json
        debate_id = data.get('debate_id')
        user_message = data.get('user_message')
        
        debate = Debate.query.get(debate_id)
        if not debate:
            print(f"Invalid debate ID: {debate_id}")
            return jsonify({'error': 'Invalid debate ID'}), 400
        
        print(f"Updating debate with ID: {debate_id}")
        print(f"User message: {user_message}")
        
        # Call OpenAI API to get LLM response
        llm_response = get_llm_response(
            user_message,
            debate.state,
            debate.topic, 
            debate.user_side, 
            debate.ai_side, 
            debate.user_responses_dict, 
            debate.llm_responses_dict
        )

        # Update LLM responses
        llm_responses = debate.llm_responses_dict
        if debate.state not in llm_responses:
            llm_responses[debate.state] = []
        llm_responses[debate.state].append(llm_response)
        debate.llm_responses_dict = llm_responses
        print(f"Updated LLM responses: {debate.llm_responses_dict}")

        # Update user responses
        user_responses = debate.user_responses_dict
        if debate.state not in user_responses:
            user_responses[debate.state] = []
        user_responses[debate.state].append(user_message)
        debate.user_responses_dict = user_responses
        print(f"Updated user responses: {debate.user_responses_dict}")
        
        # Update debate state (simple state machine for demo purposes)
        if debate.state == 'intro':
            debate.state = 'rebuttal'
        elif debate.state == 'rebuttal':
            debate.state = 'conclusion'
        elif debate.state == 'conclusion':
            debate.state = 'finished'
        
        db.session.commit()

        return jsonify({
            "message": "Responses added successfully",
            "state": debate.state,
            "user_message": user_message,
            "llm_response": llm_response
        })