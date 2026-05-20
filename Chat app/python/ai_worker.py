import os
from dotenv import load_dotenv
import requests
load_dotenv()
KEY = os.getenv("OPENAI_API_KEY")
if not KEY:
    raise SystemExit("OPENAI_API_KEY not set")
def chat(prompt):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
    body = {"model":"gpt-3.5-turbo","messages":[{"role":"system","content":"Helpful assistant."},{"role":"user","content":prompt}], "max_tokens":400}
    r = requests.post(url, headers=headers, json=body)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]
if __name__ == "__main__":
    q = input("Ask: ")
    print(chat(q))
