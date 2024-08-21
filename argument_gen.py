from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
from openai import OpenAI
import json
from topics import original_topics

client = OpenAI()

def generate_argument(topic, side):
    system_prompt = "You are an AI that generates balanced arguments for and against various topics."
    prompt = f"Provide a 200 words argument {side} the topic: {topic}"
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        model="gpt-4o-mini",
    )
    return response.choices[0].message.content.strip()

# List to store the results
results = []

# Iterate through the list of topics
for topic in original_topics:
    for side in ["FOR", "AGAINST"]:
        try:
            argument = generate_argument(topic, side)
            results.append({
                "topic": topic,
                "side": side,
                "argument": argument
            })
            # Save the results to a JSON file after each argument is generated
            with open('arguments.json', 'w') as f:
                json.dump(results, f, indent=4)
        except Exception as e:
            print(f"Error generating argument for topic '{topic}' on side '{side}': {e}")

print("All arguments generated successfully!")