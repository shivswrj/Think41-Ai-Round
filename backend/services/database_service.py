from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from backend.models.conversation import Conversation
from backend.database.setup import get_db
import json

class DatabaseService:
    def __init__(self):
        pass
    
    def store_interaction(self, interaction_data: Dict[str, Any]):
        """Store conversation interaction in database"""
        db = next(get_db())
        try:
            db_interaction = Conversation(
                conversation_id=interaction_data["conversation_id"],
                user_message=interaction_data["user_message"],
                ai_response=interaction_data["ai_response"],
                interaction_type=interaction_data["interaction_type"],
                database_results=interaction_data.get("database_results")
            )
            db.add(db_interaction)
            db.commit()
            db.refresh(db_interaction)
            return db_interaction
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def get_conversation_history(self, conversation_id: str, limit: int = 10) -> List[Dict]:
        """Get conversation history for a specific conversation"""
        db = next(get_db())
        try:
            interactions = db.query(Conversation).filter(
                Conversation.conversation_id == conversation_id
            ).order_by(Conversation.timestamp.desc()).limit(limit).all()
            
            return [
                {
                    "user_message": interaction.user_message,
                    "ai_response": interaction.ai_response,
                    "interaction_type": interaction.interaction_type,
                    "timestamp": interaction.timestamp.isoformat()
                }
                for interaction in reversed(interactions)
            ]
        finally:
            db.close()