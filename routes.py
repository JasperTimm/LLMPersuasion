from flask import request, jsonify, redirect, url_for
import os
import uuid
import random
import string
import json
from database import db
from models import User, Debate, Topic, UserInfo, all_debate_types, CopyPasteEvent, DebateLog, DebateResult
from llm_handler import get_llm_response, responses_look_sensible, generate_ratings_and_feedback
from participant_service import send_submission_info
from topics import original_topics
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# A constant for the minimum time taken to complete a debate before its considered suspicious
MIN_TIME_SPENT = 300
MAX_PASTE_LENGTH = 100
MAX_INACTIVITY_TIME = 300

def init_routes(app):
    @app.route('/create_new_user', methods=['POST'])
    def create_new_user():
        def generate_username():
            digits = ''.join(random.choice(string.digits) for _ in range(8))
            return f'u{digits}'

        def generate_password():
            letters = string.ascii_lowercase
            parts = [''.join(random.choice(letters) for _ in range(5)) for _ in range(3)]
            return '-'.join(parts)

        username = generate_username()
        password = generate_password()

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # If there's a request body, use the provided participant ID and service
        if request.json:
            participant_id = request.json.get('participantId')
            participant_service = request.json.get('service')
            new_user = User(username=username, password=hashed_password, admin=False, participant_id=participant_id, participant_service=participant_service)
        else:
            new_user = User(username=username, password=hashed_password, admin=False)

        db.session.add(new_user)
        db.session.commit()

        response = {
            'username': username,
            'password': password
        }
        return jsonify(response), 201

    @app.route('/login', methods=['POST'])
    def login():
        data = request.json
        username = data.get('username')
        password = data.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return jsonify({
                'user': {
                    'username': user.username,
                    'admin': user.admin,
                    'finished': user.finished,
                    'concluded': user.concluded
                }
            }), 200
        return jsonify({'message': 'Invalid credentials'}), 401

    @app.route('/logout', methods=['POST'])
    @login_required
    def logout():
        logout_user()
        return jsonify({'message': 'Logged out successfully'}), 200

    @app.route('/protected')
    @login_required
    def protected():
        user = User.query.get(current_user.id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': {
                'username': user.username,
                'admin': user.admin,
                'finished': user.finished,
                'concluded': user.concluded,
                'volunteer': user.participant_id is None
            }
        }), 200

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

    @app.route('/start_debate_admin', methods=['POST'])
    @login_required
    def start_debate_admin():
        user = User.query.get(current_user.id)
        if not user.admin:
            return jsonify({"error": "Unauthorized access"}), 401

        llm_model_type = request.json.get('llm_model_type', 'openai_gpt-4o-mini')
        llm_debate_type = request.json.get('llm_debate_type', 'simple')

        return start_debate_common(llm_model_type, llm_debate_type)

    def get_remaining_debate_types(user_id):
        # Get the list of debate types the user has already completed
        completed_debate_types = db.session.query(Debate.llm_debate_type).filter_by(user_id=user_id).all()
        completed_debate_types = [debate_type for (debate_type,) in completed_debate_types]
        
        # Get the list of debate types the user has not completed
        remaining_debate_types = [debate_type for debate_type in all_debate_types if debate_type not in completed_debate_types]
        
        return remaining_debate_types

    @app.route('/start_debate', methods=['POST'])
    @login_required
    def start_debate():
        remaining_debate_types = get_remaining_debate_types(current_user.id)

        if not remaining_debate_types:
            return jsonify({"error": "No new debate types available"}), 400

        # Go through ALL debates from EVERY user and count the number of each debate type
        # for each of the remaining debate types
        debate_type_counts = {}
        for debate_type in remaining_debate_types:
            debate_type_counts[debate_type] = db.session.query(Debate).filter_by(llm_debate_type=debate_type).count()

        # Sort by the lowest count and pick the type with the lowest count
        min_count = min(debate_type_counts.values())
        least_done_types = [debate_type for debate_type, count in debate_type_counts.items() if count == min_count]

        # If there's a tie, pick randomly
        chosen_debate_type = random.choice(least_done_types)

        # We only support one model type for now
        llm_model_type = 'openai_gpt-4o-mini'
        return start_debate_common(llm_model_type, chosen_debate_type)

    def start_debate_common(llm_model_type, llm_debate_type):
        debate_id = str(uuid.uuid4())

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

        # Log the debate start
        debate_log = DebateLog(
            debate_id=debate_id,
            action='start'
        )
        db.session.add(debate_log)

        db.session.commit()

        response = {
            'debate_id': debate_id,
            'topic': chosen_topic.description,
            'argument': llm_debate_type == 'argument'
        }

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

        # Log the initial position
        debate_log = DebateLog(
            debate_id=debate_id,
            action='initial_position'
        )
        db.session.add(debate_log)

        db.session.commit()
        
        response = {
            'debate_id': debate_id,
            'user_side': user_side,
            'ai_side': ai_side,
            'state': debate.state
        }
        return jsonify(response)

    @app.route('/get_argument', methods=['POST'])
    @login_required
    def get_argument():
        data = request.json
        debate_id = data.get('debate_id')
        debate = Debate.query.get(debate_id)
        if not debate:
            return jsonify({'error': 'Invalid debate ID'}), 400

        if debate.llm_debate_type != 'argument':
            return jsonify({'error': 'Debate type is not argument'}), 400

        try:
            with open('arguments.json', 'r') as f:
                arguments = json.load(f)
        except FileNotFoundError:
            return jsonify({'error': 'Arguments file not found'}), 500

        topic = Topic.query.get(debate.topic_id)
        argument = next((arg['argument'] for arg in arguments if arg['topic'] == topic.description and arg['side'] == debate.ai_side), None)
        if not argument:
            return jsonify({'error': 'Argument not found'}), 404

        response = {
            'debate_id': debate_id,
            'argument': argument
        }
        return jsonify(response), 200

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
            return jsonify({'error': 'Invalid debate ID'}), 400
        
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

        # Update user responses
        user_responses = debate.user_responses_dict
        if debate.state not in user_responses:
            user_responses[debate.state] = []
        user_responses[debate.state].append(user_message)
        debate.user_responses_dict = user_responses
        
        # Update chat history
        if update_chat_history_dict:
            debate.chat_history_dict = update_chat_history_dict
            current_phase_chat_history = update_chat_history_dict.get(debate.state, {})

        # Log the debate state
        debate_log = DebateLog(
            debate_id=debate_id,
            action=debate.state
        )
        db.session.add(debate_log)

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
        if user.admin and update_chat_history_dict:
            base_response["chat_history"] = current_phase_chat_history

        return jsonify(base_response)
    
    @app.route('/final_position', methods=['POST'])
    @login_required
    def final_position():
        user = User.query.get(current_user.id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
                
        data = request.json
        debate_id = data.get('debate_id')
        final_opinion = data.get('final_opinion')
        final_likert_score = data.get('final_likert_score')
        inactive_time = data.get('inactive_time')

        debate = Debate.query.get(debate_id)
        if not debate:
            return jsonify({'error': 'Invalid debate ID'}), 400

        debate.final_opinion = final_opinion
        debate.final_likert_score = final_likert_score
        debate.inactive_time = inactive_time

        if not user.admin:
            remaining_debate_types = get_remaining_debate_types(current_user.id)
            if not remaining_debate_types:
                user.finished = True
        
        # Arguments need to be transitioned to finished state
        if debate.llm_debate_type == 'argument':
            debate.state = 'finished'

        # Log the final position
        debate_log = DebateLog(
            debate_id=debate_id,
            action='final_position'
        )
        db.session.add(debate_log)

        db.session.commit()

        response = {
            'user_finished': user.finished,
            'message': 'Final position submitted'
        }

        return jsonify(response), 200
    
    @app.route('/finish', methods=['POST'])
    @login_required
    def finish():
        user = User.query.get(current_user.id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user.finished = True
        db.session.commit()
        
        return jsonify({'message': 'User marked as finished'}), 200
    
    @app.route('/conclude', methods=['POST'])
    @login_required
    def conclude():
        user = User.query.get(current_user.id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if not user.finished:
            return jsonify({'error': 'User must be finished before concluding'}), 400

        user.concluded = True
        db.session.commit()
        
        return jsonify({'message': 'User marked as concluded'}), 200
    
    @app.route('/log_event', methods=['POST'])
    @login_required
    def log_event():
        data = request.json
        event = CopyPasteEvent(
            type=data.get('type'),
            data=data.get('data'),
            current_page=data.get('currentPage'),
            user_id=current_user.id,
            debate_id=data.get('debateId')
        )
        db.session.add(event)
        db.session.commit()
        return '', 201

    @app.route('/get_results', methods=['GET'])
    @login_required
    def get_results():
        user_id = current_user.id

        # Check the user has concluded
        user = User.query.get(user_id)
        if not user.concluded:
            return jsonify({'error': 'User must be concluded before viewing results'}), 400
        
        # Get results for all debates for this user
        results = DebateResult.query.join(Debate).filter(Debate.user_id == user_id).all()

        # Add topic description to results
        for result in results:
            topic = Topic.query.get(Debate.query.get(result.debate_id).topic_id)
            result.topic_description = topic.description

        # Add user and AI sides to results
        for result in results:
            debate = Debate.query.get(result.debate_id)
            result.user_side = debate.user_side
            result.ai_side = debate.ai_side
            result.user_responses = debate.user_responses_dict
            result.ai_responses = debate.llm_responses_dict
            result.llm_debate_type = debate.llm_debate_type
            if debate.llm_debate_type == 'mixed':
                result.chat_history = debate.chat_history_dict

        results_list = [{
            'debateId': result.debate_id,
            'userRating': result.user_rating,
            'aiRating': result.ai_rating,
            'timeSpent': result.time_spent,
            'feedback': result.feedback_dict,
            'requiresReview': result.requires_review,
            'topicDescription': result.topic_description,
            'userSide': result.user_side,
            'aiSide': result.ai_side,
            'llmDebateType': result.llm_debate_type,
            'userResponses': result.user_responses,
            'aiResponses': result.ai_responses,
            'chatHistory': result.chat_history if hasattr(result, 'chat_history') else None,
        } for result in results]

        response_dict = {
            'results': results_list,
        }

        if user.participant_id:
            response_dict['participant'] = {
                'participantId': user.participant_id,
                'participantService': user.participant_service,
                'participantStatus': user.participant_status_dict
            }

        return jsonify(response_dict), 200
    
    @app.route('/generate_results', methods=['POST'])
    @login_required
    def generate_results():
        user_id = current_user.id

        # Check the user has concluded
        user = User.query.get(user_id)
        if not user.concluded:
            return jsonify({'error': 'User must be concluded before generating results'}), 400

        # Check if we've already generated results for this user
        results = DebateResult.query.join(Debate).filter(Debate.user_id == user_id).all()
        if results:
            return jsonify({'error': 'Results already generated'}), 400
        
        # Otherwise generate results for all debates for this user
        debates = Debate.query.filter_by(user_id=user_id).all()
        reviews_required = False
        for debate in debates:
            debate_id = debate.id

            # Check if it's simply not finished first, continue if so
            if debate.state != 'finished':
                result = DebateResult(
                    debate_id=debate_id,
                    user_rating='',
                    ai_rating='',
                    time_spent=0,
                    feedback_dict={},
                    requires_review=True,
                    review_reasons_list=['UNFINISHED']
                )
                db.session.add(result)
                continue

            # Check for suspicious activity
            start_time = DebateLog.query.filter_by(debate_id=debate_id, action='start').first().timestamp
            end_time = DebateLog.query.filter_by(debate_id=debate_id, action='final_position').first().timestamp
            time_spent = (end_time - start_time).total_seconds()

            # If it's an argument, don't bother with the rest
            if debate.llm_debate_type == 'argument':
                result = DebateResult(
                    debate_id=debate_id,
                    user_rating='',
                    ai_rating='',
                    time_spent=time_spent,
                    feedback_dict={},
                    requires_review=False
                )
                db.session.add(result)
                continue

            copy_paste_events = CopyPasteEvent.query.filter_by(debate_id=debate_id).all()
            paste_events = [event for event in copy_paste_events if event.type == 'paste']
            copy_events = [event for event in copy_paste_events if event.type == 'copy']

            # Run through list of copy events and if the data matches a paste event, remove it from paste_events
            for copy_event in copy_events:
                for paste_event in paste_events:
                    if copy_event.data == paste_event.data:
                        paste_events.remove(paste_event)
                        break
                    # Ignore pastes that are shorter than MAX_PASTE_LENGTH
                    if len(paste_event.data) < MAX_PASTE_LENGTH:
                        paste_events.remove(paste_event)
                        break

            review_reasons = []

            # Check for suspicious activity
            if time_spent < MIN_TIME_SPENT:
                review_reasons.append('SUSPICIOUS_TIME')
            if len(paste_events):
                review_reasons.append('PASTE_EVENTS')
            if debate.inactive_time > MAX_INACTIVITY_TIME:
                review_reasons.append('INACTIVE_TIME')
            
            topic = Topic.query.get(debate.topic_id)
            extended_reasons = responses_look_sensible(debate, topic.description)
            if extended_reasons:
                review_reasons.append('INSENSIBLE_RESPONSES')

            if review_reasons:
                result = DebateResult(
                    debate_id=debate_id,
                    user_rating='',
                    ai_rating='',
                    time_spent=time_spent,
                    feedback_dict={},
                    requires_review=True,
                    review_reasons_list=review_reasons,
                    extended_reasons_list=extended_reasons
                )
                db.session.add(result)
                reviews_required = True
                continue
            
            # Otherwise, continue to generate results
            ratings = generate_ratings_and_feedback(debate, topic.description)

            result = DebateResult(
                debate_id=debate_id,
                user_rating=ratings['user_rating'],
                ai_rating=ratings['opponent_rating'],
                time_spent=time_spent,
                feedback_dict=ratings['user_feedback'],
                requires_review=False
            )
            db.session.add(result)


        if user.participant_id:
            # We can approve in the API automatically using 'send_submission_info',
            # but for now we're just leaving the submission
            # in 'to review' and giving a completion code which indicates
            # whether we think we should approve or not
            if reviews_required:
                user.participant_status_dict = {
                    'status': 'NEEDS_REVIEW',
                    'completion_code': os.getenv('PROLIFIC_REVIEW_CODE')
                }
            else:
                user.participant_status_dict = {
                    'status': 'SHOULD_APPROVE',
                    'completion_code': os.getenv('PROLIFIC_APPROVAL_CODE')
                }

        db.session.commit()

        return 'Results generated', 200            