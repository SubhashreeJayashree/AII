from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def bfs_ai_response(user_query: str):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "system",
                "content": "You are an AI assistant for Banking and Financial Services. Give clear, safe, and helpful answers."
            },
            {
                "role": "user",
                "content": user_query
            }
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content
