import uvicorn
import os
from backend.api.chat_api import app
from backend.database.setup import create_tables
from backend.config.settings import settings
from flask_cors import CORS

if __name__ == "__main__":
    # Create database tables
    create_tables()
    from flask import Flask, request, jsonify
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('FLASK_ENV') == 'development'

    )
    uvicorn.run(
        "backend.api.chat_api:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )

app = Flask(__name__)

# Configure CORS
CORS(app, origins=[
    "http://localhost:3000",  # React dev server
    "http://localhost:3001",  # Alternative React port
    os.getenv("FRONTEND_URL", "http://localhost:3000")
])

# Your existing routes here...


    # Run the application
    