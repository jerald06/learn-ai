from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot import qa

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "file://", "*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

@app.get("/")
def read_root():
    return {"status": "API is running", "message": "Backend is accessible"}

@app.get("/ask")
def ask(q: str):
    answer = qa.run(q)
    return {"answer": answer}

@app.post("/ask")
def ask_question(question: Question):
    answer = qa.run(question.question)
    return {"answer": answer}