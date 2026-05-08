import os

from openai import OpenAI


def summarize_change(code_diff):
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("API_KEY")
    if not api_key:
        return "AI summary unavailable: set OPENAI_API_KEY before running the app."

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes code diffs in simple words.",
            },
            {
                "role": "user",
                "content": f"Summarize the following code diff:\n\n{code_diff}",
            },
        ],
    )
    return response.choices[0].message.content


summarize_clients = summarize_change
