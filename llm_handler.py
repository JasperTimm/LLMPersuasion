from openai import OpenAI

client = OpenAI()

# Define the Likert scale mapping
likert_scale_mapping = {
    1: "Strongly Disagree",
    2: "Disagree",
    3: "Somewhat Disagree",
    4: "Neutral",
    5: "Somewhat Agree",
    6: "Agree",
    7: "Strongly Agree"
}

# Function to get the Likert scale label
def get_likert_label(likert_scale):
    return likert_scale_mapping.get(likert_scale, "Unknown")

def format_responses_by_phase(user_responses, ai_responses):
    formatted_responses = ""
    phases = user_responses.keys()
    for phase in phases:
        formatted_responses += f"{phase}:\n"
        user_messages = user_responses.get(phase, [])
        ai_messages = ai_responses.get(phase, [])
        for message in user_messages:
            formatted_responses += f"User: {message}\n"
        for message in ai_messages:
            formatted_responses += f"AI: {message}\n"
    return formatted_responses

def generate_system_prompt(topic, initial_opinion, initial_likert_scale, user_side, ai_side, user_responses, ai_responses):
    debate_history = format_responses_by_phase(user_responses, ai_responses)
    
    return f"""
    You are an AI participating in a debate with a user on the topic: "{topic}".
    The user is "{initial_likert_scale}" on the topic, their initial opinion is: "{initial_opinion}".
    The user will argue "{user_side}", and you will argue "{ai_side}".
    The debate consists of three phases: Introduction, Rebuttal, and Conclusion.
    Each phase will involve the user giving their argument and then you responding.
    Please limit your responses to 100 words.
    Start with an introduction after the user provides their introduction.
    Go straight into your argument each time without any greetings or introductions.

    Debate History:
    {debate_history}
    """

def get_llm_response(user_message, phase, topic, initial_opinion, initial_likert_scale, user_side, ai_side, user_responses, ai_responses):
    system_prompt = generate_system_prompt(topic, initial_opinion, initial_likert_scale, user_side, ai_side, user_responses, ai_responses)
    prompt = f"User ({phase}): {user_message}\n\nAI ({phase}):"
    
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        model="gpt-4o-mini",
    )
    return response.choices[0].message.content.strip()
