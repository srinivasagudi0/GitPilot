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
        "answer": "A"
    }
    Only return the JSON object, no additional text. The questions should be based on git commands and concepts."""
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
     
    return json.loads(response.choices[0].message.content)

def practice_quiz():
    quiz = quiz_generator()
    print("\n" + "="*50)
    print("GIT QUIZ")
    print("="*50)
    print(f"\nQuestion: {quiz['question']}\n")
    for choice in quiz["choices"]:
        print(choice)
    
    user_answer = input("\nYour answer (A/B/C/D): ").strip().upper()
    correct_answer = quiz["answer"]
    
    if user_answer == correct_answer:
        print("\n✓ Correct!")
        return True
    else:
        print(f"\n✗ Incorrect. The correct answer is: {quiz['answer']}")
        return False
    
    # first test it out in cli and then integrate it into the main menu