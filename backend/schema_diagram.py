# schema_diagram.py - Visual representation of the database schema

def print_schema_diagram():
    """Print ASCII diagram of the database schema"""
    
    print("""
=== CONVERSATIONAL AI DATABASE SCHEMA ===

┌─────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│      USER       │     │    CONVERSATION     │     │      MESSAGE        │
├─────────────────┤     ├─────────────────────┤     ├─────────────────────┤
│ id (PK)         │────┐│ id (PK)             │────┐│ id (PK)             │
│ username        │    ││ user_id (FK)        │    ││ conversation_id (FK)│
│ created_at      │    │├─────────────────────┤    │├─────────────────────┤
└─────────────────┘    ││ title               │    ││ content             │
                       ││ created_at          │    ││ role                │
                       ││ updated_at          │    ││ timestamp           │
                       │└─────────────────────┘    │└─────────────────────┘
                       │                           │
                       └───────────────────────────┘

RELATIONSHIPS:
- One User can have Many Conversations (1:N)
- One Conversation can have Many Messages (1:N)
- Messages are ordered chronologically by timestamp

SCHEMA FEATURES:
✅ Supports multiple users
✅ Each user can have multiple distinct conversation sessions  
✅ Each session stores chronological sequence of queries/responses
✅ Foreign key constraints maintain data integrity
✅ Timestamps enable proper ordering and session tracking
""")

if __name__ == '__main__':
    print_schema_diagram()
