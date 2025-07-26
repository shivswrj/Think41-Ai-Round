import uvicorn
from backend.api.chat_api import app
from backend.database.setup import create_tables
from backend.config.settings import settings

if __name__ == "__main__":
    # Create database tables
    create_tables()
    
    # Run the application
    uvicorn.run(
        "backend.api.chat_api:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )