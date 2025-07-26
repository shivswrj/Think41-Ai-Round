from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String, unique=True, index=True)
    user_message = Column(Text)
    ai_response = Column(Text)
    interaction_type = Column(String)  # 'clarification', 'response', 'error'
    database_results = Column(JSON)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())