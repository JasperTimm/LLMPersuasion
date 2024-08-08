from flask import request, jsonify, redirect, url_for
import uuid
import random
from database import db
from models import User, Debate, Topic, UserInfo
from llm_handler import get_llm_response
from topics import original_topics
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

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

    @app.route('/check_user_info', methods=['GET'])
    @login_required
    def check_user_info():
        user = User.query.get(current_user.id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check user.user_info for completion
        user_info_completed = user.user_info is not None

        return jsonify({'user_info_completed': user_info_completed}), 200
    
    @app.route('/user_info', methods=['POST'])
    @login_required
    def user_info():
        user = User.query.get(current_user.id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.json

        if user.user_info is None:
            user.user_info = UserInfo()
            db.session.commit()

        # Demographics
        user.user_info.age = data.get('age')
        user.user_info.gender = data.get('gender')
        user.user_info.profession = data.get('profession')
        user.user_info.education_level = data.get('educationLevel')
        user.user_info.country_most_time = data.get('countryMostTime')
        # Personality traits
        user.user_info.extraverted_enthusiastic = data.get('extravertedEnthusiastic')
        user.user_info.critical_quarrelsome = data.get('criticalQuarrelsome')
        user.user_info.dependable_self_disciplined = data.get('dependableSelfDisciplined')
        user.user_info.anxious_easily_upset = data.get('anxiousEasilyUpset')
        user.user_info.open_to_experiences_complex = data.get('openToExperiencesComplex')
        user.user_info.reserved_quiet = data.get('reservedQuiet')
        user.user_info.sympathetic_warm = data.get('sympatheticWarm')
        user.user_info.disorganized_careless = data.get('disorganizedCareless')
        user.user_info.calm_emotionally_stable = data.get('calmEmotionallyStable')
        user.user_info.conventional_uncreative = data.get('conventionalUncreative')

        db.session.commit()

        return jsonify({'message': 'User info updated successfully'}), 200

    @app.route('/start_debate', methods=['POST'])
    @login_required
    def start_debate():
        debate_id = str(uuid.uuid4())
        llm_model_type = request.json.get('llm_model_type', 'openai_gpt-4o-mini')
        llm_debate_type = request.json.get('llm_debate_type', 'simple')

        # Get all topic IDs the user has already seen
        seen_topic_ids = db.session.query(Debate.topic_id).filter_by(user_id=current_user.id).all()
        seen_topic_ids = [topic_id for (topic_id,) in seen_topic_ids]

        # Get all topic IDs that the user has not seen
        available_topics = Topic.query.filter(~Topic.id.in_(seen_topic_ids)).all()

        if not available_topics:
            return jsonify({"error": "No new topics available"}), 400

        # Randomly choose a topic from the available topics
        chosen_topic = random.choice(available_topics)

        user = User.query.get(current_user.id)
        user.total_debates += 1

        new_debate = Debate(
            id=debate_id,
            topic_id=chosen_topic.id,
            user_side='',
            ai_side='',
            user_id=current_user.id,
            debate_count=user.total_debates,
            llm_model_type=llm_model_type,
            llm_debate_type=llm_debate_type
        )
        db.session.add(new_debate)
        db.session.commit()

        response = {
            'debate_id': debate_id,
            'topic': chosen_topic.description
        }
        print(f"Started debate with ID: {debate_id}, topic: {chosen_topic.description}, and user ID: {current_user.id}")
        return jsonify(response)

    @app.route('/initial_position', methods=['POST'])
    @login_required
    def initial_position():
        data = request.json
        debate_id = data.get('debate_id')
        initial_opinion = data.get('initial_opinion')
        initial_likert_score = data.get('initial_likert_score')

        debate = Debate.query.get(debate_id)
        if not debate:
            return jsonify({'error': 'Invalid debate ID'}), 400

        if initial_likert_score in [1, 2, 3]:
            user_side = 'AGAINST'
        elif initial_likert_score in [5, 6, 7]:
            user_side = 'FOR'
        else:
            user_side = random.choice(['FOR', 'AGAINST'])

        ai_side = 'AGAINST' if user_side == 'FOR' else 'FOR'
        debate.user_side = user_side
        debate.ai_side = ai_side
        debate.initial_opinion = initial_opinion
        debate.initial_likert_score = initial_likert_score

        db.session.commit()
        
        response = {
            'debate_id': debate_id,
            'user_side': user_side,
            'ai_side': ai_side,
            'state': debate.state
        }
        return jsonify(response)

    @app.route('/update_debate', methods=['POST'])
    @login_required
    def update_debate():
        user = User.query.get(current_user.id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.json
        debate_id = data.get('debate_id')
        user_message = data.get('user_message')
        
        debate = Debate.query.get(debate_id)
        if not debate:
            print(f"Invalid debate ID: {debate_id}")
            return jsonify({'error': 'Invalid debate ID'}), 400
        
        print(f"Updating debate with ID: {debate_id}")
        print(f"User message: {user_message}")
        
        topic = Topic.query.get(debate.topic_id)
        if not topic:
            return jsonify({"error": "Topic not found"}), 404

        llm_response, update_chat_history_dict = get_llm_response(
            user_message,
            debate.state,
            topic.description,
            debate.initial_opinion, 
            debate.initial_likert_score,            
            debate.user_side,
            debate.ai_side,
            debate.user_responses_dict,
            debate.llm_responses_dict,
            debate.llm_model_type,
            debate.llm_debate_type,
            debate.chat_history_dict,
            user.user_info
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
        
        # Update chat history
        if update_chat_history_dict:
            debate.chat_history_dict = update_chat_history_dict
            print(f"Updated chat history: {debate.chat_history_dict}")
            current_phase_chat_history = update_chat_history_dict.get(debate.state, {})
            
        # Update debate state (simple state machine for demo purposes)
        if debate.state == 'intro':
            debate.state = 'rebuttal'
        elif debate.state == 'rebuttal':
            debate.state = 'conclusion'
        elif debate.state == 'conclusion':
            debate.state = 'finished'
        
        db.session.commit()

        # Only add chat_history if it was updated
        base_response = {
            "message": "Responses added successfully",
            "state": debate.state,
            "user_message": user_message,
            "llm_response": llm_response
        }
        if update_chat_history_dict:
            base_response["chat_history"] = current_phase_chat_history

        return jsonify(base_response)
    
    @app.route('/final_position', methods=['POST'])
    @login_required
    def final_position():
        data = request.json
        debate_id = data.get('debate_id')
        final_opinion = data.get('final_opinion')
        final_likert_score = data.get('final_likert_score')

        debate = Debate.query.get(debate_id)
        if not debate:
            return jsonify({'error': 'Invalid debate ID'}), 400

        debate.final_opinion = final_opinion
        debate.final_likert_score = final_likert_score

        db.session.commit()

        response = {
            'debate_id': debate_id,
            'final_opinion': final_opinion,
            'final_likert_score': final_likert_score
        }
        return jsonify(response)    