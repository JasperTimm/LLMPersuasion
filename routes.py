from flask import request, jsonify
import uuid
import random
from database import db
from models import Debate
from llm_handler import get_llm_response

topics = ["Is artificial intelligence beneficial to society?"]

def init_routes(app):
    @app.route('/create_debate', methods=['POST'])
    def create_debate():
        data = request.json
        user_side = data.get('user_side')
        if not user_side or user_side not in ['FOR', 'AGAINST']:
            return jsonify({'error': 'user_side must be either FOR or AGAINST'}), 400
        
        ai_side = 'AGAINST' if user_side == 'FOR' else 'FOR'
        
        debate_id = str(uuid.uuid4())
        topic = random.choice(topics)
        new_debate = Debate(id=debate_id, topic=topic, user_side=user_side, ai_side=ai_side)
        db.session.add(new_debate)
        db.session.commit()
        
        response = {
            'debate_id': debate_id,
            'topic': topic
        }
        print(f"Created debate with ID: {debate_id} and topic: {topic}")
        return jsonify(response)

    @app.route('/update_debate', methods=['POST'])
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
        
        user_responses = debate.user_responses_list
        user_responses.append(user_message)
        debate.user_responses_list = user_responses
        print(f"Updated user responses: {debate.user_responses_list}")
        
        # Call OpenAI API to get LLM response
        llm_response = get_llm_response(user_message, debate.topic, debate.state, debate.user_side, debate.ai_side)
        llm_responses = debate.llm_responses_list
        llm_responses.append(llm_response)
        debate.llm_responses_list = llm_responses
        print(f"Updated LLM responses: {debate.llm_responses_list}")
        
        # Update debate state (simple state machine for demo purposes)
        if debate.state == 'intro':
            debate.state = 'rebuttal'
        elif debate.state == 'rebuttal':
            debate.state = 'conclusion'
        elif debate.state == 'conclusion':
            debate.state = 'finished'
        
        db.session.commit()
        print(f"Debate state after update: {debate.state}")
        
        response = {
            'debate_id': debate_id,
            'state': debate.state,
            'user_message': user_message,
            'llm_response': llm_response
        }
        return jsonify(response)
