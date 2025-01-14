from dotenv import dotenv_values
from openai import OpenAI

config = dotenv_values(".env")
api_key = config["OPENAI_KEY"]

client = OpenAI(api_key=api_key)

def score_job_opening(text: str) -> float:
    pass

def call_llm(system_prompt: str | None, user_prompt: str | None) -> str:
    model="gpt-4o-mini"

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    if user_prompt:
        messages.append({"role": "user", "content": user_prompt})
    
    completion = client.chat.completions.create(messages=messages, model=model)
    return completion.choices[0].message.content
