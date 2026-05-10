import os
from openai import OpenAI


def is_git_initialized(repo_dir):
    if not os.path.isdir(repo_dir):
        return False

    git_dir = os.path.join(repo_dir, ".git")
    return os.path.exists(git_dir)


def summarize_git_status(status_output):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Summarize the following git status output in simple terms:\n\n{status_output}\n\nSummary:"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes git status outputs in simple terms.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=150,
        temperature=0.5,
    )
    summary = response.choices[0].message.content.strip()
    return summary
