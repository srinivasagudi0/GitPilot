from openai import OpenAI
import os
import json
import streamlit as st



def quiz_generator(client):
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

def quiz_ui():
    st.title("Git Quiz")
    if st.button("Generate Quiz"):
        if not os.getenv("OPENAI_API_KEY"):
            st.error("Set your OpenAI API key in the environment variable OPENAI_API_KEY to use this feature.")
            return
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        quiz = quiz_generator(client)
        for i in range(4):
            choice = quiz["choices"][i]
            if st.button(choice):
                if choice.startswith(quiz["answer"]):
                    st.success("Correct!")
                else:
                    st.error(f"Incorrect. The correct answer is: {quiz['answer']}")