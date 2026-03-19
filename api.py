"""
FastAPI application for the AI Assistant.
Provides REST API endpoints for the enhanced chatbot.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from config import config
from enhanced_chatbot import chatbot

app = FastAPI(
    title="AI Assistant API",
    description="Enhanced AI Assistant with MCP MySQL Integration",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

class HealthResponse(BaseModel):
    status: str
    message: str
    database: bool = None
    user_count: int = None

@app.get("/", response_model=HealthResponse)
def read_root():
    """Health check endpoint."""
    health_data = {
        "status": "API is running",
        "message": "Backend is accessible"
    }
    
    # Test database connection
    try:
        from database import user_repository
        health_data["database"] = user_repository.db_manager.test_connection()
        health_data["user_count"] = user_repository.get_user_count()
    except Exception as e:
        health_data["database"] = False
        health_data["user_count"] = 0
    
    return health_data

@app.get("/ask")
def ask(q: str):
    """Get answer from AI assistant via GET request."""
    try:
        answer = chatbot.run(q)
        return {"answer": answer, "status": "success"}
    except Exception as e:
        return {"answer": f"Error: {str(e)}", "status": "error"}

@app.post("/ask")
def ask_question(question: Question):
    """Get answer from AI assistant via POST request."""
    try:
        answer = chatbot.run(question.question)
        return {"answer": answer, "status": "success"}
    except Exception as e:
        return {"answer": f"Error: {str(e)}", "status": "error"}

@app.get("/health")
def health_check():
    """Detailed health check endpoint."""
    try:
        test_results = chatbot.test_system()
        return {
            "status": "healthy",
            "components": test_results
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=True
    )