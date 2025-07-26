from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.services.llm_service import LLMIntegrationService
from backend.services.database_service import DatabaseService
from backend.config.settings import settings
import uuid

app = FastAPI(title="Conversational AI Backend", version="1.0.0")

# Initialize services
database_service = DatabaseService()
llm_service = LLMIntegrationService(
    groq_api_key=settings.GROQ_API_KEY,
    database_service=database_service
)

class ChatRequest(BaseModel):
    message: str
    conversation_id: str = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    type: str
    timestamp: str

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Main chat endpoint for conversational AI"""
    try:
        # Generate conversation ID if not provided
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        # Process the message
        result = llm_service.query_database_and_respond(
            request.message, 
            conversation_id
        )
        
        return ChatResponse(
            response=result["response"],
            conversation_id=conversation_id,
            type=result["type"],
            timestamp=result["timestamp"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/conversation/{conversation_id}")
async def get_conversation_history(conversation_id: str):
    """Get conversation history"""
    try:
        history = database_service.get_conversation_history(conversation_id)
        return {"conversation_id": conversation_id, "history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Conversational AI Backend"}