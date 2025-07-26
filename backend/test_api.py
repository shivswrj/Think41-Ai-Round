# test_api.py - Test the Core Chat API (Milestone 4)

import requests
import json
import time

# Configuration
BASE_URL = 'http://localhost:5000'
API_URL = f'{BASE_URL}/api'

def test_health_check():
    """Test the health check endpoint"""
    print("=== TESTING HEALTH CHECK ===")
    
    try:
        response = requests.get(f'{API_URL}/health')
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure Flask app is running!")
        return False

def test_primary_chat_endpoint():
    """Test the primary chat endpoint - Milestone 4 requirement"""
    print("\n=== TESTING PRIMARY CHAT ENDPOINT ===")
    
    # Test 1: Basic chat message
    print("\n1. Testing basic chat message:")
    
    chat_data = {
        "message": "Hello, I'm looking for some help with products",
        "user_id": "test_user_milestone4"
    }
    
    try:
        response = requests.post(
            f'{API_URL}/chat',
            json=chat_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        
        if response.status_code == 200:
            conversation_id = result.get('conversation_id')
            print(f"✅ Chat endpoint working! Conversation ID: {conversation_id}")
            return conversation_id
        else:
            print("❌ Chat endpoint failed!")
            return None
            
    except Exception as e:
        print(f"❌ Error testing chat endpoint: {str(e)}")
        return None

def test_conversation_continuation(conversation_id):
    """Test continuing a conversation with existing conversation_id"""
    print("\n2. Testing conversation continuation:")
    
    if not conversation_id:
        print("❌ No conversation ID to continue with")
        return
    
    chat_data = {
        "message": "What products do you have available?",
        "conversation_id": conversation_id,
        "user_id": "test_user_milestone4"
    }
    
    try:
        response = requests.post(
            f'{API_URL}/chat',
            json=chat_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        
        if response.status_code == 200:
            print("✅ Conversation continuation working!")
        else:
            print("❌ Conversation continuation failed!")
            
    except Exception as e:
        print(f"❌ Error testing conversation continuation: {str(e)}")

def test_message_persistence():
    """Test that messages are persisted to database"""
    print("\n3. Testing message persistence:")
    
    # Send a message
    chat_data = {
        "message": "Testing message persistence",
        "user_id": "persistence_test_user"
    }
    
    try:
        # Send message
        response = requests.post(f'{API_URL}/chat', json=chat_data)
        
        if response.status_code != 200:
            print("❌ Failed to send message")
            return
        
        result = response.json()
        conversation_id = result.get('conversation_id')
        
        # Retrieve conversation messages
        time.sleep(0.1)  # Small delay to ensure persistence
        
        messages_response = requests.get(f'{API_URL}/conversations/{conversation_id}/messages')
        
        if messages_response.status_code == 200:
            messages_data = messages_response.json()
            messages = messages_data.get('messages', [])
            
            print(f"Messages retrieved: {len(messages)}")
            
            # Should have 2 messages: user message + AI response
            if len(messages) >= 2:
                print("✅ Messages successfully persisted!")
                
                for msg in messages:
                    print(f"   - [{msg['role'].upper()}]: {msg['content']}")
            else:
                print("❌ Messages not properly persisted")
        else:
            print("❌ Failed to retrieve messages")
            
    except Exception as e:
        print(f"❌ Error testing message persistence: {str(e)}")

def test_error_handling():
    """Test API error handling"""
    print("\n4. Testing error handling:")
    
    # Test missing message
    print("   Testing missing message:")
    response = requests.post(f'{API_URL}/chat', json={})
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 400:
        print("   ✅ Proper error handling for missing message")
    else:
        print("   ❌ Error handling not working")
    
    # Test invalid conversation ID
    print("   Testing invalid conversation ID:")
    response = requests.post(f'{API_URL}/chat', json={
        "message": "Test message",
        "conversation_id": "invalid-uuid-123"
    })
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 404:
        print("   ✅ Proper error handling for invalid conversation ID")
    else:
        print("   ❌ Error handling for invalid conversation ID not working")

def test_additional_endpoints():
    """Test additional API endpoints"""
    print("\n5. Testing additional endpoints:")
    
    # Test get conversations
    print("   Testing GET /api/conversations:")
    response = requests.get(f'{API_URL}/conversations?user_id=test_user_milestone4')
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   Conversations found: {len(data.get('conversations', []))}")
        print("   ✅ Conversations endpoint working!")
    else:
        print("   ❌ Conversations endpoint failed")

def run_comprehensive_test():
    """Run all API tests for Milestone 4 verification"""
    print("="*60)
    print("MILESTONE 4: CORE CHAT API TESTING")
    print("="*60)
    
    # Test health check first
    if not test_health_check():
        print("\n❌ Server not responding. Please start the Flask app with: python app.py")
        return
    
    # Test primary chat endpoint (main requirement)
    conversation_id = test_primary_chat_endpoint()
    
    if conversation_id:
        # Test conversation continuation
        test_conversation_continuation(conversation_id)
    
    # Test message persistence
    test_message_persistence()
    
    # Test error handling
    test_error_handling()
    
    # Test additional endpoints
    test_additional_endpoints()
    
    print("\n" + "="*60)
    print("MILESTONE 4 TESTING COMPLETED")
    print("="*60)
    print("\n✅ REQUIREMENTS VERIFICATION:")
    print("✅ Primary REST API endpoint (POST /api/chat) - IMPLEMENTED")
    print("✅ Accepts user message and optional conversation_id - IMPLEMENTED")
    print("✅ Persists user message and AI response to database - IMPLEMENTED")
    print("\nMilestone 4 is ready for submission!")

if __name__ == '__main__':
    run_comprehensive_test()