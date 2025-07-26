# test_schema.py - Test queries to verify schema functionality

import sqlite3

def test_schema_queries():
    """Test various queries to ensure schema works correctly"""
    
    conn = sqlite3.connect('conversational_ai.db')
    cursor = conn.cursor()
    
    print("=== TESTING SCHEMA WITH SAMPLE QUERIES ===\n")
    
    # Query 1: Get all users and their conversation counts
    print("1. Users and their conversation counts:")
    cursor.execute('''
        SELECT u.username, COUNT(c.id) as conversations
        FROM user u
        LEFT JOIN conversation c ON u.id = c.user_id
        GROUP BY u.id, u.username
        ORDER BY conversations DESC
    ''')
    
    for username, count in cursor.fetchall():
        print(f"   {username}: {count} conversations")
    
    # Query 2: Get latest conversation for each user
    print("\n2. Latest conversation for each user:")
    cursor.execute('''
        SELECT u.username, c.title, c.updated_at
        FROM user u
        JOIN conversation c ON u.id = c.user_id
        WHERE c.updated_at = (
            SELECT MAX(updated_at) 
            FROM conversation c2 
            WHERE c2.user_id = u.id
        )
        ORDER BY c.updated_at DESC
    ''')
    
    for username, title, updated_at in cursor.fetchall():
        print(f"   {username}: {title} (Updated: {updated_at})")
    
    # Query 3: Get message history for a specific conversation
    print("\n3. Complete message thread (chronological):")
    cursor.execute('''
        SELECT m.role, m.content, m.timestamp
        FROM message m
        JOIN conversation c ON m.conversation_id = c.id
        JOIN user u ON c.user_id = u.id
        WHERE u.username = 'alice_smith'
        ORDER BY m.timestamp ASC
        LIMIT 10
    ''')
    
    for role, content, timestamp in cursor.fetchall():
        print(f"   [{role.upper()}] {content[:50]}... ({timestamp})")
    
    conn.close()

if __name__ == '__main__':
    test_schema_queries()
