from openai import OpenAI
import  os
import json

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def quiz_generator():
    prompt = """Generate a multiple choice question with 4 answer options and the correct answer.
    Return the response as a JSON object with the following structure:
    {
        "question": "The question text",
        "choices": [
            "A) First option",
            "B) Second option",
            "C) Third option",
            "D) Fourth option"
        ],
        "answer": "A) Correct answer text"
    }
    Only return the JSON object, no additional text."""
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt + "The questions should be based on git commands and concepts."}]
    )
    
    return json.loads(response.choices[0].message.content)