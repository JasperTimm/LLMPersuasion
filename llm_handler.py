from openai import OpenAI

client = OpenAI()

def generate_system_prompt(topic, user_side, ai_side):
    return f"""
    You are an AI participating in a debate with a user on the topic: "{topic}".
    The user will argue "{user_side}", and you will argue "{ai_side}".
    The debate consists of three phases: Introduction, Rebuttal, and Conclusion.
    Each phase will involve you and the user taking turns to present your arguments.
    Please limit your responses to 100 words.
    Start with an introduction after the user provides their introduction.
    """

def get_llm_response(user_message, topic, phase, user_side, ai_side):
    system_prompt = generate_system_prompt(topic, user_side, ai_side)
    prompt = f"{system_prompt}\n\nUser ({phase}): {user_message}\n\nAI ({phase}):"
    
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_message}
        ],
        max_tokens=1500,
        model="gpt-4o"
    )
    return response.choices[0].message.content.strip()
