from fastapi import FastAPI
from pydantic import BaseModel
from ai import bfs_ai_response

app = FastAPI(title="BFS AI Assistant")

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask_bfs_ai(query: Query):
    answer = bfs_ai_response(query.question)
    return {
        "question": query.question,
        "answer": answer
    }
