#!/bin/bash
# test_curl.sh - Quick curl tests for the Chat API

echo "=== MILESTONE 4: CHAT API CURL TESTS ==="
echo

echo "1. Health Check:"
curl -X GET http://localhost:5000/api/health
echo -e "\n"

echo "2. Send Chat Message:"
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, I need help with your products",
    "user_id": "curl_test_user"
  }'
echo -e "\n"

echo "3. Get API Documentation:"
curl -X GET http://localhost:5000/api/docs
echo -e "\n"

echo "4. Get Conversations:"
curl -X GET "http://localhost:5000/api/conversations?user_id=curl_test_user"
echo -e "\n"