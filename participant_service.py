import os
import requests
from flask import jsonify

def send_submission_info(user, reviews_required):
    participant_service = user.participant_service
    participant_id = user.participant_id
    internal_server_error = {
        'status': 'ERROR',
        'error': 'Internal Server Error'
    }

    if participant_service == 'amazon':
        return ({
            'status': 'ERROR',
            'error': 'Amazon service is not supported'})

    if participant_service == 'prolific':
        api_token = os.getenv('PROLIFIC_API_TOKEN')
        if not api_token:
            print('PROLIFIC_API_TOKEN not set!')
            return internal_server_error

        headers = {
            'Authorization': f'token {api_token}'
        }

        # Get list of submissions
        study_id = os.getenv('PROLIFIC_STUDY_ID')
        if not study_id:
            print('PROLIFIC_STUDY_ID not set!')
            return internal_server_error
        
        submissions_url = f"https://api.prolific.com/api/v1/studies/{study_id}/submissions/"
        response = requests.get(submissions_url, headers=headers)
        if response.status_code != 200:
            print(f"Error getting submissions: {response.text}")
            return internal_server_error

        submissions = response.json()['results']
        submission_id = None
        for submission in submissions:
            if submission['participant_id'] == participant_id and submission['status'] == 'ACTIVE':
                submission_id = submission['id']
                break

        if not submission_id:
            return ({
                'status': 'ERROR',
                'error': 'No ACTIVE submission found for this participant ID'})

        completion_code = os.getenv('PROLIFIC_COMPLETION_CODE')
        if not completion_code:
            print('PROLIFIC_COMPLETION_CODE not set!')
            return internal_server_error

        # Complete the submission first, setting to 'AWAITING_REVIEW'
        transition_url = f'https://api.prolific.com/api/v1/submissions/{submission_id}/transition/'
        transition_data = {
            'action': 'COMPLETE',
            'completion_code': completion_code,
        }
        response = requests.post(transition_url, headers=headers, json=transition_data)
        if response.status_code != 200:
            print(f"Error completing submission: {response.text}")
            return internal_server_error

        # Approve if reviews are not required
        if not reviews_required:
            transition_data = {
                'action': 'APPROVE'
            }
            response = requests.post(transition_url, headers=headers, json=transition_data)
            if response.status_code != 200:
                print(f"Error approving submission: {response.text}")
                return internal_server_error
            return ({
                'status': 'APPROVED'})
        else:
            return ({
                'status': 'AWAITING_REVIEW'})

    return ({
        'status': 'ERROR',
        'error': 'Unknown participant service'})