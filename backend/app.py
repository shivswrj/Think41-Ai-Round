# app.py - Milestone 4: Core Chat API Implementation (Fixed)

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
import os

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///conversational_ai.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models (using SQLAlchemy ORM)
class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    conversations = db.relationship('Conversation', backref='user', lazy=True)

class Conversation(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), default="New Conversation")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    messages = db.relationship('Message', backref='conversation', lazy=True, cascade='all, delete-orphan')

class Message(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = db.Column(db.String(36), db.ForeignKey('conversation.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'user' or 'assistant'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'content': self.content,
            'role': self.role,
            'timestamp': self.timestamp.isoformat()
        }

# Simple AI Response Generator (placeholder for Milestone 5)
class SimpleAIService:
    """Simple AI service that generates responses based on user input"""
    
    def generate_response(self, user_message, conversation_history=None):
        """Generate a simple AI response based on user input"""
        
        user_message_lower = user_message.lower()
        
        # Simple response logic
        if 'hello' in user_message_lower or 'hi' in user_message_lower:
            return "Hello! How can I help you today?"
        elif 'product' in user_message_lower or 'buy' in user_message_lower:
            return "I can help you find products. We have electronics, accessories, and more. What are you looking for?"
        elif 'price' in user_message_lower or 'cost' in user_message_lower:
            return "Our products are competitively priced. Would you like me to check specific item prices for you?"
        elif 'thank' in user_message_lower:
            return "You're welcome! Is there anything else I can help you with?"
        elif 'bye' in user_message_lower or 'goodbye' in user_message_lower:
            return "Goodbye! Feel free to come back anytime if you need assistance."
        else:
            return f"I understand you're asking about: '{user_message}'. Let me help you with that. Could you provide more details about what you're looking for?"

ai_service = SimpleAIService()

# MILESTONE 4: PRIMARY CHAT API ENDPOINT
@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Primary REST API endpoint for chat functionality
    
    Accepts:
    - message (required): User's message
    - conversation_id (optional): Existing conversation ID
    - user_id (optional): User identifier (defaults to 'default_user')
    
    Returns:
    - JSON response with conversation_id, messages, and AI response
    """
    try:
        # Validate request data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        if 'message' not in data or not data['message'].strip():
            return jsonify({'error': 'Message is required and cannot be empty'}), 400
        
        user_message = data['message'].strip()
        conversation_id = data.get('conversation_id')
        user_id = data.get('user_id', 'default_user')
        
        print(f"[API] Received message from {user_id}: {user_message[:50]}...")
        
        # Step 1: Get or create user
        user = User.query.filter_by(username=user_id).first()
        if not user:
            user = User(username=user_id)
            db.session.add(user)
            db.session.flush()  # Get the ID without committing
            print(f"[API] Created new user: {user_id}")
        
        # Step 2: Get or create conversation
        if conversation_id:
            conversation = Conversation.query.filter_by(
                id=conversation_id, 
                user_id=user.id
            ).first()
            if not conversation:
                return jsonify({'error': 'Conversation not found'}), 404
            print(f"[API] Using existing conversation: {conversation_id}")
        else:
            # Create new conversation
            conversation = Conversation(
                user_id=user.id,
                title=f"Chat - {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"
            )
            db.session.add(conversation)
            db.session.flush()  # Get the ID without committing
            print(f"[API] Created new conversation: {conversation.id}")
        
        # Step 3: Get conversation history for context
        history = Message.query.filter_by(
            conversation_id=conversation.id
        ).order_by(Message.timestamp.asc()).all()
        
        conversation_context = [msg.to_dict() for msg in history]
        
        # Step 4: Save user message to database
        user_msg = Message(
            conversation_id=conversation.id,
            content=user_message,
            role='user'
        )
        db.session.add(user_msg)
        
        # Step 5: Generate AI response
        ai_response = ai_service.generate_response(user_message, conversation_context)
        print(f"[API] Generated AI response: {ai_response[:50]}...")
        
        # Step 6: Save AI response to database
        ai_msg = Message(
            conversation_id=conversation.id,
            content=ai_response,
            role='assistant'
        )
        db.session.add(ai_msg)
        
        # Step 7: Update conversation timestamp
        conversation.updated_at = datetime.utcnow()
        
        # Step 8: Commit all changes to database
        db.session.commit()
        
        print(f"[API] Successfully persisted messages to database")
        
        # Step 9: Return response
        response_data = {
            'success': True,
            'conversation_id': conversation.id,
            'user_message': {
                'id': user_msg.id,
                'content': user_message,
                'role': 'user',
                'timestamp': user_msg.timestamp.isoformat()
            },
            'ai_response': {
                'id': ai_msg.id,
                'content': ai_response,
                'role': 'assistant',
                'timestamp': ai_msg.timestamp.isoformat()
            },
            'conversation_title': conversation.title,
            'message_count': len(history) + 2  # Previous messages + new user message + AI response
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        # Rollback database changes on error
        db.session.rollback()
        print(f"[API ERROR] {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500

# Additional API endpoints for conversation management
@app.route('/api/conversations', methods=['GET'])
def get_conversations():
    """Get all conversations for a user"""
    user_id = request.args.get('user_id', 'default_user')
    
    user = User.query.filter_by(username=user_id).first()
    if not user:
        return jsonify({'conversations': []})
    
    conversations = Conversation.query.filter_by(user_id=user.id).order_by(
        Conversation.updated_at.desc()
    ).all()
    
    result = []
    for conv in conversations:
        # Get message count
        message_count = Message.query.filter_by(conversation_id=conv.id).count()
        
        # Get last message
        last_message = Message.query.filter_by(
            conversation_id=conv.id
        ).order_by(Message.timestamp.desc()).first()
        
        result.append({
            'id': conv.id,
            'title': conv.title,
            'created_at': conv.created_at.isoformat(),
            'updated_at': conv.updated_at.isoformat(),
            'message_count': message_count,
            'last_message': last_message.content[:100] + '...' if last_message and len(last_message.content) > 100 else (last_message.content if last_message else None),
            'last_message_role': last_message.role if last_message else None
        })
    
    return jsonify({
        'user_id': user_id,
        'conversations': result,
        'total_conversations': len(result)
    })

@app.route('/api/conversations/<conversation_id>/messages', methods=['GET'])
def get_conversation_messages(conversation_id):
    """Get all messages in a conversation"""
    conversation = Conversation.query.get(conversation_id)
    if not conversation:
        return jsonify({'error': 'Conversation not found'}), 404
    
    messages = Message.query.filter_by(
        conversation_id=conversation_id
    ).order_by(Message.timestamp.asc()).all()
    
    result = [msg.to_dict() for msg in messages]
    
    return jsonify({
        'conversation_id': conversation_id,
        'conversation_title': conversation.title,
        'messages': result,
        'total_messages': len(result)
    })

@app.route('/api/conversations/<conversation_id>', methods=['DELETE'])
def delete_conversation(conversation_id):
    """Delete a conversation and all its messages"""
    conversation = Conversation.query.get(conversation_id)
    if not conversation:
        return jsonify({'error': 'Conversation not found'}), 404
    
    # Delete conversation (messages will be deleted automatically due to cascade)
    db.session.delete(conversation)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Conversation deleted successfully',
        'conversation_id': conversation_id
    })

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        user_count = User.query.count()
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0',
            'database_connected': True,
            'total_users': user_count
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

# API documentation endpoint
@app.route('/api/docs', methods=['GET'])
def api_docs():
    """API documentation"""
    docs = {
        'title': 'Conversational AI Backend API',
        'version': '1.0.0',
        'description': 'Core Chat API for conversational AI system',
        'endpoints': {
            'POST /api/chat': {
                'description': 'Send a message and get AI response',
                'parameters': {
                    'message': 'string (required) - User message',
                    'conversation_id': 'string (optional) - Existing conversation ID',
                    'user_id': 'string (optional) - User identifier'
                },
                'response': 'JSON with conversation_id, user_message, ai_response'
            },
            'GET /api/conversations': {
                'description': 'Get all conversations for a user',
                'parameters': {
                    'user_id': 'string (optional) - User identifier'
                }
            },
            'GET /api/conversations/{id}/messages': {
                'description': 'Get all messages in a conversation'
            },
            'DELETE /api/conversations/{id}': {
                'description': 'Delete a conversation'
            },
            'GET /api/health': {
                'description': 'Health check endpoint'
            }
        }
    }
    return jsonify(docs)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'available_endpoints': [
            'POST /api/chat',
            'GET /api/conversations',
            'GET /api/conversations/{id}/messages',
            'DELETE /api/conversations/{id}',
            'GET /api/health',
            'GET /api/docs'
        ]
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 'Method not allowed for this endpoint'
    }), 405

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

# Initialize database tables when the app starts
def init_database():
    """Initialize database tables"""
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables created successfully!")
            return True
        except Exception as e:
            print(f"❌ Database initialization failed: {str(e)}")
            return False

if __name__ == '__main__':
    print("Starting Conversational AI Backend Service...")
    print("="*50)
    
    # Initialize database
    if init_database():
        print("✅ Flask application ready!")
        print("\nAvailable endpoints:")
        print("- POST /api/chat (Primary chat endpoint)")
        print("- GET /api/conversations")
        print("- GET /api/conversations/{id}/messages")
        print("- DELETE /api/conversations/{id}")
        print("- GET /api/health")
        print("- GET /api/docs")
        print(f"\n🚀 Server starting on http://localhost:5000")
        print("="*50)
        
        # Run the Flask application
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ Failed to initialize database. Exiting...")